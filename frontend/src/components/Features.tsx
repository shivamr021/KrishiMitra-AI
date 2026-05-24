import { motion } from "framer-motion";
import { Sprout, Bug, Droplets, TrendingUp } from "lucide-react";

const features = [
  {
    icon: Sprout,
    title: "Smart Crop Recommendations",
    description: "Get personalized crop suggestions based on your location, season, weather patterns, and soil conditions for maximum yield.",
    gradient: "from-primary to-leaf-dark",
  },
  {
    icon: Bug,
    title: "Pest & Disease Detection",
    description: "Simply upload a photo of your affected crop. Our AI identifies issues early and provides treatment recommendations to prevent losses.",
    gradient: "from-earth-dark to-earth",
  },
  {
    icon: Droplets,
    title: "Efficient Water Usage Tips",
    description: "Receive smart irrigation guidance based on weather forecasts and crop needs. Save water while improving crop health.",
    gradient: "from-accent to-primary",
  },
  {
    icon: TrendingUp,
    title: "Market Price Insights",
    description: "Access real-time crop prices from nearby markets. Know the best time to sell and maximize your profits.",
    gradient: "from-leaf-dark to-accent",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 40 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6 },
  },
};

const Features = () => {
  return (
    <section id="features" className="py-20 md:py-32 earth-gradient relative overflow-hidden">
      {/* Decorative Elements */}
      <div className="absolute top-1/4 right-0 w-72 h-72 bg-accent/10 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 left-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl" />

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
            Features
          </span>
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-6">
            Everything You Need to{" "}
            <span className="text-primary">Grow Better</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Powerful AI tools designed specifically for the needs of Indian farmers, accessible through simple WhatsApp messages.
          </p>
        </motion.div>

        {/* Feature Cards */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              variants={cardVariants}
              whileHover={{ y: -8, scale: 1.02 }}
              className="group relative bg-card rounded-2xl overflow-hidden shadow-card hover:shadow-hover transition-all duration-300"
            >
              {/* Gradient Top Bar */}
              <div className={`h-2 bg-gradient-to-r ${feature.gradient}`} />

              <div className="p-8">
                {/* Icon */}
                <motion.div
                  whileHover={{ rotate: 5 }}
                  className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-6 shadow-soft`}
                >
                  <feature.icon className="w-8 h-8 text-primary-foreground" />
                </motion.div>

                {/* Content */}
                <h3 className="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>

              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default Features;
