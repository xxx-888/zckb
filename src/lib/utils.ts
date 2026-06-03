import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { useCallback, useRef, useState } from 'react'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * 将评论图片数据统一转为 url 字符串数组
 * 兼容格式: string | { url: string } | { thumbUrl: string, url: string }
 */
export function normalizeImageUrls(images: any): string[] {
  if (!images || !Array.isArray(images)) return []
  return images.map((img: any) => {
    if (typeof img === 'string') return img
    if (img && typeof img === 'object') {
      return img.url || img.originUrl || img.bigUrl || img.thumbUrl || ''
    }
    return ''
  }).filter(Boolean)
}

/**
 * 通用搜索防抖 hook
 * 返回 [inputValue, handleChange]
 * - inputValue: 用于绑定 input 的 value（实时更新，不卡顿）
 * - debouncedValue: 防抖后的值，传给 useEffect 触发搜索
 * - handleChange: 用于 input 的 onChange（同时更新实时值和防抖）
 */
export function useSearchDebounce(delay: number = 300) {
  const [inputValue, setInputValue] = useState('')
  const [debouncedValue, setDebouncedValue] = useState('')
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const handleChange = useCallback((value: string) => {
    setInputValue(value)
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)
  }, [delay])

  return { inputValue, debouncedValue, handleChange }
}
