import { motion } from "framer-motion";
import { MessageSquare, Brain, Lightbulb, CheckCircle } from "lucide-react";

const steps = [
  {
    icon: MessageSquare,
    step: "01",
    title: "Send a Message",
    description: "Farmer sends a text, voice message, or photo of their crop on WhatsApp.",
    color: "bg-accent",
  },
  {
    icon: Brain,
    step: "02",
    title: "AI Understands",
    description: "KrishiMitra's AI analyzes the query, understanding context and language.",
    color: "bg-primary",
  },
  {
    icon: Lightbulb,
    step: "03",
    title: "Insights Generated",
    description: "Relevant insights and actionable guidance are generated instantly.",
    color: "bg-leaf-dark",
  },
  {
    icon: CheckCircle,
    step: "04",
    title: "Advice Delivered",
    description: "Farmer receives clear, actionable advice in their preferred language.",
    color: "bg-earth-dark",
  },
];

const HowItWorks = () => {
  return (
    <section id="how-it-works" className="py-20 md:py-32 hero-gradient relative overflow-hidden">
      {/* Decorative Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 left-10 w-40 h-40 border-2 border-primary-foreground rounded-full" />
        <div className="absolute bottom-20 right-20 w-60 h-60 border-2 border-primary-foreground rounded-full" />
        <div className="absolute top-1/2 left-1/2 w-32 h-32 border-2 border-primary-foreground rounded-full -translate-x-1/2 -translate-y-1/2" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block text-white font-semibold text-sm uppercase tracking-wider mb-4 bg-accent/40 px-4 py-1 rounded-full">
            How It Works
          </span>
          <h2 className="text-3xl md:text-5xl font-bold text-primary-foreground mb-6">
            Simple Steps to <span className="text-card-foreground">Smarter Farming</span>
          </h2>
          <p className="text-primary-foreground/80 text-lg max-w-2xl mx-auto">
            Getting help is as easy as sending a WhatsApp message. Here's how it works:
          </p>
        </motion.div>

        {/* Steps */}
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 relative">
            {/* Connection Line */}
            <div className="hidden md:block absolute top-16 left-[12%] right-[12%] h-0.5 bg-primary-foreground/20">
              <motion.div
                initial={{ width: 0 }}
                whileInView={{ width: "100%" }}
                viewport={{ once: true }}
                transition={{ duration: 1.5, delay: 0.5 }}
                className="h-full bg-accent"
              />
            </div>

            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.2 + index * 0.15 }}
                className="relative text-center"
              >
                {/* Step Number & Icon */}
                <div className="relative inline-block mb-6">
                  <motion.div
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    className={`w-24 h-24 ${step.color} rounded-2xl flex items-center justify-center shadow-lg mx-auto relative z-10`}
                  >
                    <step.icon className="w-10 h-10 text-primary-foreground" />
                  </motion.div>
                  <span className="absolute -top-2 -right-2 w-8 h-8 bg-primary-foreground text-primary rounded-full flex items-center justify-center font-bold text-sm z-20">
                    {step.step}
                  </span>
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-primary-foreground mb-3">
                  {step.title}
                </h3>
                <p className="text-primary-foreground/70 text-sm leading-relaxed">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
