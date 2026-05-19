import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from 'lucide-react'
import { cn } from '../../lib/utils'
import type { Toast } from '../../hooks/use-toast'

interface ToasterProps {
  toasts: Toast[]
  removeToast: (id: string) => void
}

export function Toaster({ toasts, removeToast }: ToasterProps) {
  const getToastIcon = (type: string) => {
    switch (type) {
      case 'success': return <CheckCircle className="w-4 h-4 text-emerald-500" />
      case 'error': return <AlertCircle className="w-4 h-4 text-rose-500" />
      case 'warning': return <AlertTriangle className="w-4 h-4 text-amber-500" />
      case 'info': return <Info className="w-4 h-4 text-blue-500" />
      default: return null
    }
  }

  const getToastBg = (type: string) => {
    switch (type) {
      case 'success': return 'bg-emerald-50 border-emerald-200'
      case 'error': return 'bg-rose-50 border-rose-200'
      case 'warning': return 'bg-amber-50 border-amber-200'
      case 'info': return 'bg-blue-50 border-blue-200'
      default: return 'bg-white border-slate-200'
    }
  }

  if (toasts.length === 0) return null

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-xs">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={cn(
            'flex items-start gap-3 p-4 rounded-xl border shadow-lg animate-in slide-in-from-right duration-300',
            getToastBg(toast.type)
          )}
        >
          <div className="flex-shrink-0 mt-0.5">
            {getToastIcon(toast.type)}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-slate-800">{toast.title}</p>
            {toast.description && (
              <p className="text-xs text-slate-500 mt-1">{toast.description}</p>
            )}
          </div>
          <button
            onClick={() => removeToast(toast.id)}
            className="flex-shrink-0 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      ))}
    </div>
  )
}

export default Toaster
