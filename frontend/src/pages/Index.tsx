import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Challenges from "@/components/Challenges";
import Solution from "@/components/Solution";
import Features from "@/components/Features";
import WhyWhatsApp from "@/components/WhyWhatsApp";
import HowItWorks from "@/components/HowItWorks";
import FutureVision from "@/components/FutureVision";
import Impact from "@/components/Impact";
import Footer from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <Challenges />
      <Solution />
      <Features />
      <WhyWhatsApp />
      <HowItWorks />
      <FutureVision />
      <Impact />
      <Footer />
    </div>
  );
};

export default Index;
