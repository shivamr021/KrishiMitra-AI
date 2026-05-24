import { motion } from "framer-motion";
import { TrendingDown, Clock, Bug, Languages } from "lucide-react";

const challenges = [
  {
    icon: TrendingDown,
    title: "Unpredictable Market Prices",
    description: "Farmers struggle with volatile crop prices, often selling at a loss due to lack of real-time market information.",
    color: "text-destructive",
    bgColor: "bg-destructive/10",
  },
  {
    icon: Clock,
    title: "Delayed Expert Advisory",
    description: "Getting timely advice from agricultural experts is difficult, leading to missed opportunities and crop damage.",
    color: "text-earth-dark",
    bgColor: "bg-earth-light",
  },
  {
    icon: Bug,
    title: "Pest & Water Management",
    description: "Identifying pests early and managing water efficiently remains a challenge without proper guidance.",
    color: "text-primary",
    bgColor: "bg-leaf-light",
  },
  {
    icon: Languages,
    title: "Language Barriers",
    description: "Most agricultural information is in English, while farmers prefer Hindi or their regional languages.",
    color: "text-accent",
    bgColor: "bg-accent/10",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6 },
  },
};

const Challenges = () => {
  return (
    <section id="challenges" className="py-20 md:py-32 earth-gradient relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-0 left-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-accent/5 rounded-full blur-3xl translate-x-1/3 translate-y-1/3" />

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
            The Problem
          </span>
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-6">
            Challenges Faced by{" "}
            <span className="text-primary">Indian Farmers</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Despite being the backbone of our nation, farmers face numerous obstacles that impact their livelihood and crop yield.
          </p>
        </motion.div>

        {/* Challenge Cards */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          className="grid md:grid-cols-2 gap-6 lg:gap-8 max-w-5xl mx-auto"
        >
          {challenges.map((challenge, index) => (
            <motion.div
              key={index}
              variants={itemVariants}
              className="group relative"
            >
              <div className="bg-card rounded-2xl p-8 shadow-card hover:shadow-hover transition-all duration-300 border border-border hover:border-primary/20 h-full">
                {/* Icon */}
                <div className={`w-14 h-14 ${challenge.bgColor} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <challenge.icon className={`w-7 h-7 ${challenge.color}`} />
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">
                  {challenge.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {challenge.description}
                </p>

                {/* Decorative Corner */}
                <div className="absolute top-4 right-4 w-8 h-8 border-t-2 border-r-2 border-border rounded-tr-xl opacity-50 group-hover:border-primary/30 transition-colors" />
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default Challenges;
