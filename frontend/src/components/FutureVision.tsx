import { motion } from "framer-motion";
import { Globe, Mic, Wifi, Handshake } from "lucide-react";

const visionItems = [
  {
    icon: Globe,
    title: "More Regional Languages",
    description: "Expanding support to cover all major Indian languages for truly inclusive access.",
  },
  {
    icon: Mic,
    title: "Voice-Based Interaction",
    description: "Hands-free farming assistance through natural voice conversations.",
  },
  {
    icon: Wifi,
    title: "Offline Support",
    description: "Access critical information even in areas with limited connectivity.",
  },
  {
    icon: Handshake,
    title: "Government Integration",
    description: "Seamless connection with government schemes and subsidies for farmers.",
  },
];

const FutureVision = () => {
  return (
    <section className="py-20 md:py-32 bg-background relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute top-0 left-0 w-full h-full">
        <div className="absolute top-1/4 left-10 w-32 h-32 bg-accent/5 rounded-full blur-2xl" />
        <div className="absolute bottom-1/4 right-10 w-48 h-48 bg-primary/5 rounded-full blur-3xl" />
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
          <span className="inline-block text-accent font-semibold text-sm uppercase tracking-wider mb-4">
            Future Vision
          </span>
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-6">
            Growing <span className="text-primary">Together</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            We're just getting started. Here's our roadmap to make KrishiMitra 
            even more powerful and accessible for every farmer in India.
          </p>
        </motion.div>

        {/* Vision Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {visionItems.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -5 }}
              className="bg-card rounded-2xl p-6 border border-border hover:border-primary/30 transition-all duration-300 shadow-soft hover:shadow-card text-center"
            >
              <motion.div
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
                className="w-14 h-14 mx-auto mb-4 rounded-xl bg-leaf-light flex items-center justify-center"
              >
                <item.icon className="w-7 h-7 text-primary" />
              </motion.div>
              <h3 className="font-bold text-foreground mb-2">{item.title}</h3>
              <p className="text-sm text-muted-foreground">{item.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FutureVision;
