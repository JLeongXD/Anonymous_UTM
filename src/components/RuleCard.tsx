import React from 'react';

interface RuleCardProps {
  title: string;
  content: string;
  icon: React.ReactNode;
}

export const RuleCard: React.FC<RuleCardProps> = ({ title, content, icon }) => {
  return (
    <div className="flex items-center gap-4 p-4 bg-[#17212b] rounded-lg border border-[#2b5278]/30">
      <div className="text-[#5288c1] shrink-0">
        {icon}
      </div>
      <div>
        <h3 className="font-bold text-sm text-white mb-1">
          {title}
        </h3>
        <p className="text-sm text-[#7f91a4] leading-tight">
          {content}
        </p>
      </div>
    </div>
  );
};