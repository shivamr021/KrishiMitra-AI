import { motion } from "framer-motion";
import { Sparkles, Smartphone, MessageSquare, Heart } from "lucide-react";

const solutionPoints = [
  {
    icon: Sparkles,
    title: "AI-Powered Guidance",
    description: "Instant, intelligent farming advice powered by advanced AI technology.",
  },
  {
    icon: Smartphone,
    title: "Works on WhatsApp",
    description: "No new apps to download. Use the platform you already know and trust.",
  },
  {
    icon: MessageSquare,
    title: "Simple Chat Interface",
    description: "Just send a message or photo. Get clear, actionable advice instantly.",
  },
  {
    icon: Heart,
    title: "Built for Everyone",
    description: "Designed for farmers with varying levels of digital literacy.",
  },
];

const Solution = () => {
  return (
    <section className="py-20 md:py-32 bg-background relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-20 left-10 w-32 h-32 border border-primary/20 rounded-full" />
        <div className="absolute bottom-40 right-20 w-48 h-48 border border-accent/20 rounded-full" />
        <div className="absolute top-1/2 left-1/3 w-20 h-20 border border-leaf-light rounded-full" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-block text-accent font-semibold text-sm uppercase tracking-wider mb-4">
              Our Solution
            </span>
            <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-6 leading-tight">
              Meet <span className="text-gradient">KrishiMitra-AI</span>
            </h2>
            <p className="text-muted-foreground text-lg mb-8 leading-relaxed">
              Your AI-powered farming companion that bridges the information gap. 
              We bring expert agricultural guidance directly to your fingertips through 
              WhatsApp – in your language, whenever you need it.
            </p>

            {/* Trust Badges */}
            <div className="flex flex-wrap gap-4 mb-8">
              <div className="flex items-center gap-2 bg-leaf-light/50 rounded-full px-4 py-2">
                <span className="w-2 h-2 bg-accent rounded-full" />
                <span className="text-sm font-medium text-foreground">Market Price Agent</span>
              </div>
              <div className="flex items-center gap-2 bg-leaf-light/50 rounded-full px-4 py-2">
                <span className="w-2 h-2 bg-primary rounded-full" />
                <span className="text-sm font-medium text-foreground">Regional Languages</span>
              </div>
              <div className="flex items-center gap-2 bg-leaf-light/50 rounded-full px-4 py-2">
                <span className="w-2 h-2 bg-earth-dark rounded-full" />
                <span className="text-sm font-medium text-foreground">Weather Agent</span>
              </div>
            </div>
          </motion.div>

          {/* Right - Solution Points */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="grid sm:grid-cols-2 gap-6"
          >
            {solutionPoints.map((point, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
                whileHover={{ y: -5 }}
                className="bg-card rounded-2xl p-6 shadow-soft hover:shadow-card transition-all duration-300 border border-border"
              >
                <div className="w-12 h-12 hero-gradient rounded-xl flex items-center justify-center mb-4">
                  <point.icon className="w-6 h-6 text-primary-foreground" />
                </div>
                <h3 className="font-bold text-foreground mb-2">{point.title}</h3>
                <p className="text-sm text-muted-foreground">{point.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Solution;
