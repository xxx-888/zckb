import React from 'react';
import { cn } from '../../lib/utils';

interface SkeletonProps {
  className?: string;
  lines?: number;
  avatar?: boolean;
  card?: boolean;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  className = '',
  lines = 1,
  avatar = false,
  card = false,
}) => {
  if (card) {
    return (
      <div className={cn('animate-pulse', className)}>
        <div className="h-32 bg-slate-200 rounded-2xl"></div>
      </div>
    );
  }

  if (avatar) {
    return (
      <div className={cn('animate-pulse flex items-center gap-4', className)}>
        <div className="w-10 h-10 bg-slate-200 rounded-full flex-shrink-0"></div>
        <div className="flex-1 space-y-2">
          {Array.from({ length: lines }).map((_, i) => (
            <div key={i} className="h-4 bg-slate-200 rounded w-full"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={cn('animate-pulse space-y-2', className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="h-4 bg-slate-200 rounded"></div>
      ))}
    </div>
  );
};
