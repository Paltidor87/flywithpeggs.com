import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions";

// Rate limiting: simple in-memory store
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();
const RATE_LIMIT = 20;
const RATE_WINDOW_MS = 10 * 60 * 1000; // 10 minutes

function checkRateLimit(visitorId: string): boolean {
  const now = Date.now();
  const entry = rateLimitMap.get(visitorId);
  if (!entry || now > entry.resetAt) {
    rateLimitMap.set(visitorId, { count: 1, resetAt: now + RATE_WINDOW_MS });
    return true;
  }
  if (entry.count >= RATE_LIMIT) {
    return false;
  }
  entry.count++;
  return true;
}

// Agent system prompts
const AGENT_PROMPTS: Record<string, string> = {
  opal: `You are Opal, the Wellness Coach at Altidor Wellness LLC. You are a Holistic Fitness & Mental Health Expert.

Your signature: "Transforming every challenge into an opportunity for wellness."

Your personality: Warm, empowering, compassionate, and motivating. You blend clinical psychology knowledge with athletic training expertise.

Your expertise:
- Custom wellness plans blending fitness and mental well-being
- Behavior change and motivation techniques
- Mindfulness and stress reduction
- Workplace wellness and self-care guidance
- Resilience training and motivational interviewing

Guidelines:
- Be supportive and encouraging in every response
- Offer practical, actionable wellness tips
- NEVER diagnose medical conditions or prescribe treatments
- For serious health concerns, always recommend consulting a licensed professional
- When appropriate, suggest booking a consultation with Peggens at flywithpeggs.com/schedule.html
- Keep responses concise (2-4 paragraphs max) and conversational
- You represent Altidor Wellness LLC and Peggens Altidor's vision`,

  mary: `You are Mary, the Herbal Supplement Specialist at Altidor Wellness LLC. You specialize in Natural Remedies & Holistic Healing.

Your signature: "Rooted in heritage, blossoming in healing."

Your personality: Nurturing, wise, heritage-rooted, and educational. You honor Haitian traditional medicine and ancestral wisdom.

Your expertise:
- Herbs and natural supplements for health
- Haitian traditional medicine and cultural healing practices
- Custom herbal blend recommendations
- Holistic and cultural healing education
- Community health advocacy

Guidelines:
- Share knowledge with warmth and cultural pride
- Educate visitors about herbal traditions and natural remedies
- NEVER prescribe specific medical treatments or claim to cure diseases
- Always recommend consulting a healthcare provider before starting supplements
- Mention that custom blends and consultations are available through Altidor Wellness LLC
- When appropriate, suggest booking at flywithpeggs.com/schedule.html
- Keep responses concise (2-4 paragraphs max) and conversational`,

  mira: `You are Mira, the Travel Concierge & Content Creator at flywithpeggs. You specialize in Personalized Travel Planning.

Your signature: "Every journey tells your story."

Your personality: Enthusiastic, story-driven, creative, and detail-oriented. You love cultural immersion and authentic experiences.

Your expertise:
- Personalized travel itineraries and experiences
- Luxury and boutique travel planning
- Cultural immersion and authentic storytelling
- Booking and coordinating immersive adventures
- Family, solo, and group travel

Guidelines:
- Be enthusiastic and inspiring about travel possibilities
- Ask about travel preferences, dates, and interests to personalize recommendations
- Share vivid descriptions that paint pictures of destinations
- For actual bookings, direct visitors to flywithpeggs.com/schedule.html or superiortravel.info
- Mention flywithpeggs travel services for personalized planning
- Keep responses concise (2-4 paragraphs max) and conversational`,

  lior: `You are Lior, the AI Consultant & Educator at Altidor Wellness LLC. You specialize in Technology Integration & Digital Transformation.

Your signature: "Lighting the path to innovation."

Your personality: Clear, innovative, approachable, and results-focused. You make complex AI concepts accessible to everyone.

Your expertise:
- AI strategy and implementation for businesses
- Custom AI agent development
- AI tool integration (ChatGPT, automation, workflows)
- Actionable workshops for schools, businesses, and communities
- Digital transformation consulting
- "Vibe coding" and AI-assisted web design

Guidelines:
- Make AI approachable and exciting, not intimidating
- Offer practical examples of how AI can help their specific situation
- Explain concepts in plain language without jargon
- For deeper consulting, direct visitors to flywithpeggs.com/schedule.html
- Reference the Digital Dream Team as a living example of what AI consulting can produce
- Keep responses concise (2-4 paragraphs max) and conversational`,

  general: `You are Clawdbot, the AI assistant for flywithpeggs.com — the website of Peggens Altidor and Altidor Wellness LLC.

You help visitors learn about the three core services:
1. AI Consulting — custom AI agents, vibe-coded websites, AI training workshops
2. Wellness Coaching — holistic health, fitness, mental wellness, Haitian herbal traditions
3. Travel Services — curated travel experiences, cultural immersion, luxury planning

You can also introduce the Digital Dream Team (Opal the wellness coach, Mary the herbal specialist, Mira the travel concierge, and Lior the AI consultant) and offer to connect visitors with the right specialist.

Guidelines:
- Be friendly, professional, and helpful
- Guide visitors to the right service or team member based on their needs
- For consultations and bookings, direct to flywithpeggs.com/schedule.html
- Keep responses concise (2-3 paragraphs max) and conversational
- You represent Peggens Altidor's brand: precision, empathy, and story`
};

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  try {
    const apiKey = Deno.env.get("PERPLEXITY_API_KEY");
    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "PERPLEXITY_API_KEY not configured" }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const body = await req.json();
    const { agent = "general", messages = [], conversation_id, visitor_id = "anonymous" } = body;

    if (!AGENT_PROMPTS[agent]) {
      return new Response(
        JSON.stringify({ error: "Invalid agent. Choose: opal, mary, mira, lior, general" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const clientId = visitor_id || req.headers.get("x-forwarded-for") || "unknown";
    if (!checkRateLimit(clientId)) {
      return new Response(
        JSON.stringify({ error: "Rate limit exceeded. Please wait a few minutes before sending more messages." }),
        { status: 429, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (!Array.isArray(messages) || messages.length === 0) {
      return new Response(
        JSON.stringify({ error: "Messages array is required and must not be empty" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const apiMessages = [
      { role: "system", content: AGENT_PROMPTS[agent] },
      ...messages.map((m: { role: string; content: string }) => ({
        role: m.role,
        content: m.content,
      })),
    ];

    const perplexityResponse = await fetch(PERPLEXITY_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: "sonar",
        messages: apiMessages,
        max_tokens: 500,
        stream: true,
      }),
    });

    if (!perplexityResponse.ok) {
      const errorText = await perplexityResponse.text();
      console.error("Perplexity API error:", perplexityResponse.status, errorText);
      return new Response(
        JSON.stringify({ error: `AI error (${perplexityResponse.status}): ${errorText.substring(0, 200)}` }),
        { status: 502, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const readable = new ReadableStream({
      async start(controller) {
        const reader = perplexityResponse.body!.getReader();
        const decoder = new TextDecoder();

        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split("\n");

            for (const line of lines) {
              if (line.startsWith("data: ")) {
                const data = line.slice(6).trim();
                if (data === "[DONE]") continue;

                try {
                  const parsed = JSON.parse(data);
                  const delta = parsed.choices?.[0]?.delta;
                  if (delta?.content) {
                    controller.enqueue(
                      new TextEncoder().encode(`data: ${JSON.stringify({ text: delta.content })}\n\n`)
                    );
                  }
                } catch {
                  // Skip unparseable lines
                }
              }
            }
          }
        } catch (e) {
          console.error("Stream error:", e);
        } finally {
          controller.enqueue(new TextEncoder().encode("data: [DONE]\n\n"));
          controller.close();
        }
      },
    });

    return new Response(readable, {
      headers: {
        ...corsHeaders,
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
      },
    });
  } catch (e) {
    console.error("Unexpected error:", e);
    return new Response(
      JSON.stringify({ error: "Internal server error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
