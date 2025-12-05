import React, { useState, useRef, useEffect } from 'react';
import { Share2, Info, User, VenetianMask, ExternalLink, Paperclip, Send as SendIcon, X, Check, ChevronRight } from 'lucide-react';
import { BOT_LINK } from './constants';
import { RuleCard } from './components/RuleCard';

const App: React.FC = () => {
  const [showRules, setShowRules] = useState(false);
  const [selectedMode, setSelectedMode] = useState<'anonymous' | 'named' | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  //auto scroll去底部when selectedMode changes
  useEffect(() => {
    if (selectedMode && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [selectedMode]);

  //点击按钮会打开telegrambot
  const handleLinkToBot = () => {
    window.open(BOT_LINK, '_blank'); 
  };

  //user可以copy当前页面link
  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      alert("Link copied to clipboard!");
    } catch (err) {
      console.error("Failed to copy", err);
    }
  };

  //加粗(**text**) 和 换行
  const formatText = (text: string) => {
    return text.split('\n').map((line, i) => (
      <React.Fragment key={i}>
        {line.split(/(\*\*.*?\*\*)/).map((part, j) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return <b key={j} className="text-white">{part.slice(2, -2)}</b>;
          }
          return part;
        })}
        <br />
      </React.Fragment>
    ));
  };

//Bot主页面显示的内容 when user selects anonymous mode
  const anonymousText = `🕵️ **Anonymous Mode Activated**

✅ You are now in Anonymous Mode.
- Your identity will **not** be shown when your submission is posted.
- You can send **text messages** or **images** freely.

💡 Tip: Keep your messages clear and concise for the audience.`;

//Bot主页面显示的内容 when user selects named mode
  const namedText = `👤 **Named Mode Activated**
Displayed Name: **'Your ID Name'**

✅ You are now in Named Mode.
- Your full name will be visible with your su bmission.
- You can send **text messages** or **images**.

💡 Tip: Make sure you are comfortable sharing your name publicly.`;

  return (
    //大小和布局
    <div className="flex flex-col h-[100dvh] max-w-md mx-auto relative shadow-2xl">
      
      {/* ---Header--- */}
      <header className="flex items-center justify-between px-4 py-3 bg-[#17212b]/95 backdrop-blur-md sticky top-0 z-10 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="flex flex-col">
            <h1 className="font-bold text-white text-[17px] leading-tight">Anonymous_UTM_bot</h1>
            <span className="text-[#6c7883] text-xs">bot</span>
          </div>
        </div>
        <button onClick={handleShare} className="text-[#ffffff] hover:text-blue-400 transition-colors p-2">
          <Share2 size={20} />
        </button>
      </header>

      {/* ---Chat Content--- */}
      <main className="flex-1 overflow-y-auto px-4 py-6 flex flex-col gap-6 scroll-smooth">
        
        {/* 1.Welcome Message Bubble */}
        <div className="flex gap-2 max-w-[90%] animate-in slide-in-from-left-2 duration-300">
          <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 self-end mb-1">
             <img src="https://api.dicebear.com/9.x/bottts-neutral/svg?seed=UTM123" alt="Bot" className="bg-[#17212b]" />
          </div>
          <div className="glass-panel p-4 rounded-2xl rounded-bl-none text-[15px] leading-relaxed relative text-white/90">
            <p className="mb-4">
              Welcome to <b>Anonymous_UTM_bot</b>.
            </p>
            <p className="mb-2">
              Everything here is encrypted and anonymous. Choose a mode to start sharing your secrets.
            </p>
            <span className="text-[11px] text-white/40 absolute bottom-2 right-3">01:05 AM</span>
          </div>
        </div>

        {/* 2.Action Buttons List (The Menu) */}
        <div className="flex flex-col gap-3 px-1 mt-2">
          
          {/* Anonymous Mode Button */}
          <button 
            onClick={() => setSelectedMode('anonymous')} 
            className={`glass-button w-full p-4 rounded-xl flex items-center justify-between group transition-all active:scale-95 ${selectedMode === 'anonymous' ? 'border-yellow-400/50 bg-yellow-400/10' : ''}`}
          >
            <div className="flex items-center gap-4">
              <span className="text-yellow-400">
                <VenetianMask size={24} />
              </span>
              <span className="font-semibold text-[15px]">Anonymous Mode</span>
            </div>
            {selectedMode === 'anonymous' ? <Check size={18} className="text-yellow-400"/> : <ChevronRight size={18} className="text-white/30" />}
          </button>

          {/*Named Mode Button*/}
          <button 
            onClick={() => setSelectedMode('named')} 
            className={`glass-button w-full p-4 rounded-xl flex items-center justify-between group transition-all active:scale-95 ${selectedMode === 'named' ? 'border-blue-400/50 bg-blue-400/10' : ''}`}
          >
            <div className="flex items-center gap-4">
              <span className="text-blue-400">
                <User size={24} />
              </span>
              <span className="font-semibold text-[15px]">Named Mode</span>
            </div>
            {selectedMode === 'named' ? <Check size={18} className="text-blue-400"/> : <ChevronRight size={18} className="text-white/30" />}
          </button>

          {/*How it works Button*/}
          <button onClick={() => setShowRules(true)} className="glass-button w-full p-4 rounded-xl flex items-center justify-between group transition-all active:scale-95">
            <div className="flex items-center gap-4">
              <span className="text-white/70">
                <Info size={24} />
              </span>
              <span className="font-semibold text-[15px]">How it works</span>
            </div>
            <ExternalLink size={18} className="text-white/30 group-hover:text-white/60" />
          </button>

        </div>

        {/*3.Conditional Bot Response*/}
        {selectedMode && (
          <div className="flex flex-col gap-2 max-w-[95%] self-start animate-in fade-in slide-in-from-bottom-4 duration-500 fill-mode-forwards">
             <div className="flex gap-2">
                <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 self-end mb-1">
                  <img src="https://api.dicebear.com/9.x/bottts-neutral/svg?seed=UTM123" alt="Bot" className="bg-[#17212b]" />
                </div>
                <div className="glass-panel p-4 rounded-2xl rounded-bl-none text-[14px] leading-relaxed relative text-gray-200 shadow-lg">
                  <div className="whitespace-pre-wrap">
                    {formatText(selectedMode === 'anonymous' ? anonymousText : namedText)}
                  </div>
                  <span className="text-[11px] text-white/40 block text-right mt-2">Just now</span>
                </div>
             </div>
             
             {/*Submit Button (Link to Telegram)*/}
             <div className="pl-10 pr-2">
                <button 
                  onClick={handleLinkToBot}
                  className="w-full bg-[#5288c1] hover:bg-[#4674a6] text-white font-bold py-3 px-4 rounded-xl shadow-lg flex items-center justify-center gap-2 transition-all active:scale-95 border border-white/10"
                >
                  <span>Submit your message now!</span>
                  <SendIcon size={16} />
                </button>
             </div>
          </div>
        )}

        {/*Spacer for scrolling*/}
        <div ref={messagesEndRef} className="h-4" />
      </main>

      {/*--- Footer/Fake Input ---*/}
      <footer className="px-2 pb-2 pt-0 sticky bottom-0 z-10">
        <div className="bg-[#17212b] p-2 rounded-b-none rounded-t-xl mx-2 flex flex-col items-center shadow-[0_-4px_20px_rgba(0,0,0,0.3)] border-t border-white/5">
             <div className="w-full flex items-center gap-3 bg-[#0e1621] px-4 py-3 rounded-[20px] border border-white/5 opacity-50 pointer-events-none">
                <Paperclip size={22} className="text-[#6c7883] rotate-45" />
                <div className="flex-1 text-[#6c7883] text-[15px]">Write a confession...</div>
                <SendIcon size={22} className="text-[#6c7883]" />
             </div>
             <div className="text-[10px] text-[#485665] font-bold tracking-widest mt-3 mb-1">
                HAVE A GOOD DAY! :D
             </div>
        </div>
      </footer>

      {/*--- Rules Modal ---*/}
      {showRules && (
        <div className="absolute inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-[#17212b] w-full max-w-sm rounded-xl overflow-hidden shadow-2xl border border-white/10 animate-in zoom-in-95 duration-200">
            {/*Modal Header*/}
            <div className="flex items-center justify-between p-4 border-b border-white/5 bg-[#232e3c]">
              <h2 className="font-bold text-lg">How it works</h2>
              <button onClick={() => setShowRules(false)} className="p-1 hover:bg-white/10 rounded-full">
                <X size={20} className="text-gray-400" />
              </button>
            </div>
            
            {/*Modal Content*/}
            <div className="p-4 space-y-3 max-h-[60vh] overflow-y-auto">
               <RuleCard 
                title="Anonymous Mode" 
                icon={<VenetianMask size={18} />}
                content="Your identity is completely hidden. Messages are sent without your name."
              />
              <RuleCard 
                title="Named Mode" 
                icon={<User size={18} />}
                content="Your full Telegram name will be displayed with your confession."
              />
              <RuleCard 
                title="AI Moderation" 
                icon={<Info size={18} />}
                content="Gemini AI reviews all content. Nudity, violence, and hate speech are blocked."
              />
              
              <div className="mt-4 pt-2 border-t border-white/5">
                 <p className="text-xs text-gray-400 text-center">Click any mode button to start the bot.</p>
              </div>
            </div>
            
            <div className="p-3 bg-[#0e1621]">
               <button 
                onClick={() => setShowRules(false)}
                className="w-full py-3 bg-[#5288c1] text-white font-bold rounded-lg active:scale-95 transition-transform"
               >
                 Got it
               </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default App;