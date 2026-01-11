import { motion } from "framer-motion";
import { Smartphone, Download, MessageCircle, Mic, Image, Check } from "lucide-react";

const benefits = [
  {
    icon: Download,
    title: "No App Installation",
    description: "Works directly on WhatsApp. No downloads, no setup, no hassle.",
  },
  {
    icon: Smartphone,
    title: "Works on Basic Phones",
    description: "Compatible with entry-level smartphones that most farmers use.",
  },
  {
    icon: MessageCircle,
    title: "Familiar Interface",
    description: "Farmers already know how to use WhatsApp. Zero learning curve.",
  },
  {
    icon: Image,
    title: "Easy Image Sharing",
    description: "Just click and send crop photos for instant disease detection.",
  },
];

const WhyWhatsApp = () => {
  return (
    <section className="py-20 md:py-32 bg-background relative overflow-hidden">
      {/* WhatsApp Green Accent */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-accent/10 rounded-full blur-3xl translate-x-1/2 -translate-y-1/2" />

      <div className="container mx-auto px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left - Phone Mockup */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6 }}
            className="relative flex justify-center"
          >
            <div className="relative">
              {/* Phone Frame */}
              <div className="w-72 md:w-80 h-[580px] md:h-[620px] bg-foreground rounded-[3rem] p-3 shadow-2xl">
                <div className="w-full h-full bg-background rounded-[2.5rem] overflow-hidden relative">
                  {/* WhatsApp Header */}
                  <div className="bg-accent text-accent-foreground p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-accent-foreground/20 flex items-center justify-center">
                      <span className="text-lg">🌾</span>
                    </div>
                    <div>
                      <p className="font-semibold">KrishiMitra-AI</p>
                      <p className="text-xs opacity-80">Online</p>
                    </div>
                  </div>

                  {/* Chat Messages */}
                  <div className="p-4 space-y-3 bg-leaf-light/20">
                    {/* User Message */}
                    <motion.div
                      initial={{ opacity: 0, x: 20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.3 }}
                      className="flex justify-end"
                    >
                      <div className="bg-accent/20 rounded-2xl rounded-tr-sm px-4 py-2 max-w-[80%]">
                        <p className="text-sm text-foreground">मेरी फसल में कीड़े लग गए हैं। क्या करूं?</p>
                        <p className="text-xs text-muted-foreground text-right mt-1">10:30 AM</p>
                      </div>
                    </motion.div>

                    {/* Bot Response */}
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.5 }}
                      className="flex justify-start"
                    >
                      <div className="bg-card rounded-2xl rounded-tl-sm px-4 py-3 max-w-[85%] shadow-soft">
                        <p className="text-sm text-foreground mb-2">
                          नमस्ते! 🙏 कृपया प्रभावित फसल की फोटो भेजें, मैं समस्या पहचानने में मदद करूंगा।
                        </p>
                        <p className="text-xs text-muted-foreground">10:31 AM ✓✓</p>
                      </div>
                    </motion.div>

                    {/* Image Message */}
                    <motion.div
                      initial={{ opacity: 0, x: 20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.7 }}
                      className="flex justify-end"
                    >
                      <div className="bg-accent/20 rounded-2xl rounded-tr-sm p-2 max-w-[60%]">
                        <div className="w-full h-24 bg-leaf-light/50 rounded-xl flex items-center justify-center">
                          <Image className="w-8 h-8 text-primary/50" />
                        </div>
                        <p className="text-xs text-muted-foreground text-right mt-1">10:32 AM</p>
                      </div>
                    </motion.div>

                    {/* Bot Final Response */}
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.9 }}
                      className="flex justify-start"
                    >
                      <div className="bg-card rounded-2xl rounded-tl-sm px-4 py-3 max-w-[85%] shadow-soft">
                        <p className="text-sm text-foreground">
                          यह <span className="font-semibold text-primary">एफिड्स (माहू)</span> का प्रकोप है। नीम तेल का छिड़काव करें। 🌿
                        </p>
                        <p className="text-xs text-muted-foreground mt-1">10:33 AM ✓✓</p>
                      </div>
                    </motion.div>
                  </div>
                </div>
              </div>

              {/* Floating Badge */}
              <motion.div
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute -right-4 top-20 bg-accent text-accent-foreground px-4 py-2 rounded-full shadow-lg font-semibold text-sm"
              >
                💬 WhatsApp
              </motion.div>
            </div>
          </motion.div>

          {/* Right Content */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-block text-accent font-semibold text-sm uppercase tracking-wider mb-4">
              Why WhatsApp?
            </span>
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-6">
              The Platform Farmers{" "}
              <span className="text-accent">Already Trust</span>
            </h2>
            <p className="text-muted-foreground text-lg mb-8">
              We chose WhatsApp because it's already in every farmer's pocket. 
              No new apps to learn, no barriers to access.
            </p>

            {/* Benefits List */}
            <div className="space-y-4">
              {benefits.map((benefit, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: 20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.2 + index * 0.1 }}
                  className="flex items-start gap-4 group"
                >
                  <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center flex-shrink-0 group-hover:bg-accent/20 transition-colors">
                    <benefit.icon className="w-5 h-5 text-accent" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground mb-1">{benefit.title}</h3>
                    <p className="text-sm text-muted-foreground">{benefit.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default WhyWhatsApp;
