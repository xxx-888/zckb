import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from 'lucide-react'
import { cn } from '../../lib/utils'
import type { Toast } from '../../hooks/use-toast'

interface ToasterProps {
  toasts: Toast[]
  removeToast: (id: string) => void
}

const toastConfig = {
  success: {
    icon: <CheckCircle className="w-[18px] h-[18px] text-white" />,
    gradient: 'from-emerald-400 to-emerald-600',
    accent: 'bg-emerald-400',
    progress: 'bg-emerald-400',
  },
  error: {
    icon: <AlertCircle className="w-[18px] h-[18px] text-white" />,
    gradient: 'from-rose-400 to-rose-600',
    accent: 'bg-rose-400',
    progress: 'bg-rose-400',
  },
  warning: {
    icon: <AlertTriangle className="w-[18px] h-[18px] text-white" />,
    gradient: 'from-amber-400 to-amber-600',
    accent: 'bg-amber-400',
    progress: 'bg-amber-400',
  },
  info: {
    icon: <Info className="w-[18px] h-[18px] text-white" />,
    gradient: 'from-blue-400 to-blue-600',
    accent: 'bg-blue-400',
    progress: 'bg-blue-400',
  },
} as const

export function Toaster({ toasts, removeToast }: ToasterProps) {
  if (toasts.length === 0) return null

  return (
    <>
      {/* 桌面端：右上角 */}
      <div className="hidden md:flex fixed top-5 right-5 z-[100] flex-col gap-2.5 w-full max-w-[380px]">
        {toasts.map((toast, i) => (
          <ToastItem key={toast.id} toast={toast} removeToast={removeToast} index={i} />
        ))}
      </div>

      {/* 移动端：顶部居中 */}
      <div className="flex md:hidden fixed top-3 left-1/2 -translate-x-1/2 z-[100] flex-col gap-2.5 w-[calc(100%-1.5rem)] max-w-sm">
        {toasts.map((toast, i) => (
          <ToastItem key={toast.id} toast={toast} removeToast={removeToast} index={i} />
        ))}
      </div>
    </>
  )
}

function ToastItem({ toast, removeToast, index }: { toast: Toast; removeToast: (id: string) => void; index: number }) {
  const config = toastConfig[toast.type as keyof typeof toastConfig] || toastConfig.info

  return (
    <div
      className={cn(
        // 深色半透明玻璃 — 在浅色页面上依然清晰可见
        'relative flex items-start gap-3 p-3.5 pr-10 rounded-2xl overflow-hidden',
        'bg-slate-900/80 backdrop-blur-xl',
        'border border-white/10',
        'shadow-[0_12px_48px_rgba(0,0,0,0.45)]',
        // 入场动画
        'opacity-0 -translate-y-2 scale-[0.97]',
        'animate-[toast-in_0.4s_cubic-bezier(0.16,1,0.3,1)_both]',
      )}
      style={{ animationDelay: `${index * 60}ms` } as React.CSSProperties}
    >
      {/* 左侧色彩条 */}
      <div className={cn('absolute left-[3px] top-3 bottom-3 w-[2.5px] rounded-full', config.accent)} />

      {/* 图标：渐变圆角方块 */}
      <div className={cn(
        'flex-shrink-0 flex items-center justify-center w-8 h-8 rounded-xl mt-0.5',
        'bg-gradient-to-br shadow-md',
        config.gradient
      )}>
        {config.icon}
      </div>

      {/* 文字内容 */}
      <div className="flex-1 min-w-0 pt-0.5">
        <p className="text-[13px] font-semibold text-white leading-snug">{toast.title}</p>
        {toast.description && (
          <p className="text-[12px] text-white/50 mt-0.5 leading-relaxed line-clamp-2">{toast.description}</p>
        )}
      </div>

      {/* 关闭按钮 */}
      <button
        onClick={() => removeToast(toast.id)}
        className="absolute top-2 right-2 flex items-center justify-center w-6 h-6 rounded-lg
                   text-white/30 hover:text-white/80 hover:bg-white/10 transition-all duration-200"
      >
        <X className="w-3.5 h-3.5" />
      </button>

      {/* 底部自动消失进度条 */}
      <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-white/5">
        <div
          className={cn('h-full rounded-full', config.progress)}
          style={{ animation: 'toast-shrink 3s linear forwards', animationDelay: '0.5s' } as React.CSSProperties}
        />
      </div>
    </div>
  )
}

export default Toaster
