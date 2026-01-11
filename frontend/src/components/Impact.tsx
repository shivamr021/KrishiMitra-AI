import { motion } from "framer-motion";
import { TrendingUp, ShieldCheck, Leaf, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { MessageCircle } from "lucide-react";

const impacts = [
  {
    icon: TrendingUp,
    stat: "Better Decisions",
    description: "Data-driven farming choices for improved outcomes",
  },
  {
    icon: ShieldCheck,
    stat: "Reduced Losses",
    description: "Early detection prevents crop damage and waste",
  },
  {
    icon: Users,
    stat: "Income Stability",
    description: "Market insights help farmers earn fairly",
  },
  {
    icon: Leaf,
    stat: "Sustainable Farming",
    description: "Eco-friendly practices for a greener future",
  },
];

const Impact = () => {
  const handleOnClick = ()=>{
    const phoneNumber = "+14155238886";
    const message = "join plenty-engine";
    window.open(`https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`,"_blank")
  }
  return (
    <section id="impact" className="py-20 md:py-32 earth-gradient relative overflow-hidden">
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
            Our Impact
          </span>
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-6">
            Changes We <span className="text-primary">Drive</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Every conversation on KrishiMitra helps build a more sustainable and 
            prosperous future for Indian agriculture.
          </p>
        </motion.div>

        {/* Impact Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto mb-16">
          {impacts.map((impact, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="bg-card rounded-2xl p-6 text-center shadow-card border border-border"
            >
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-accent/10 flex items-center justify-center">
                <impact.icon className="w-8 h-8 text-accent" />
              </div>
              <h3 className="font-bold text-foreground text-lg mb-2">{impact.stat}</h3>
              <p className="text-sm text-muted-foreground">{impact.description}</p>
            </motion.div>
          ))}
        </div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl mx-auto text-center bg-card rounded-3xl p-8 md:p-12 shadow-card border border-border"
        >
          <h3 className="text-2xl md:text-4xl font-bold text-foreground mb-4">
            Ready to Transform Your Farming?
          </h3>
          <p className="text-lg text-accent font-semibold italic mb-6">
            "Harvesting Knowledge, Sowing Success."
          </p>
          <p className="text-muted-foreground mb-8">
            Join thousands of farmers who are already using KrishiMitra-AI to 
            make smarter decisions and improve their yield.
          </p>
          <Button variant="whatsapp" size="xl" className="group" onClick={handleOnClick}>
            <MessageCircle className="w-5 h-5 group-hover:animate-pulse" />
            Start Your Journey on WhatsApp
          </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default Impact;
