import { Leaf, Mail, Phone, MapPin } from "lucide-react";

const Footer = () => {
  const currentYear = new Date().getFullYear();
  const krishimitraemail = "krishimitra2.ai@gmail.com"
  return (
    <footer className="bg-primary text-primary-foreground py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-xl bg-accent flex items-center justify-center">
                <Leaf className="w-6 h-6 text-accent-foreground" />
              </div>
              <span className="font-display font-bold text-xl">
                KrishiMitra<span className="text-accent">-AI</span>
              </span>
            </div>
            <p className="text-primary-foreground/70 text-sm leading-relaxed max-w-md">
              Empowering Indian farmers with AI-driven insights through WhatsApp. 
              Bridging the information gap for a more sustainable and prosperous agricultural future.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-display font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#home" className="text-primary-foreground/70 hover:text-accent transition-colors">Home</a></li>
              <li><a href="#challenges" className="text-primary-foreground/70 hover:text-accent transition-colors">Challenges</a></li>
              <li><a href="#features" className="text-primary-foreground/70 hover:text-accent transition-colors">Features</a></li>
              <li><a href="#how-it-works" className="text-primary-foreground/70 hover:text-accent transition-colors">How It Works</a></li>
              <li><a href="#impact" className="text-primary-foreground/70 hover:text-accent transition-colors">Impact</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-display font-semibold mb-4">Contact</h4>
            <ul className="space-y-3 text-sm">
              <li className="flex items-center gap-2 text-primary-foreground/70">
                <Mail className="w-4 h-4" />
                <a href={`mailto:${krishimitraemail}`}>{krishimitraemail}</a>
              </li>
              <li className="flex items-center gap-2 text-primary-foreground/70">
                <Phone className="w-4 h-4" />
                +91 9340761474
              </li>
              <li className="flex items-start gap-2 text-primary-foreground/70">
                <MapPin className="w-4 h-4 mt-0.5" />
                India
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-primary-foreground/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-primary-foreground/60 text-sm">
            © {currentYear} KrishiMitra-AI. All rights reserved.
          </p>
          <p className="text-primary-foreground/60 text-sm italic">
            "Harvesting Knowledge, Sowing Success."
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
