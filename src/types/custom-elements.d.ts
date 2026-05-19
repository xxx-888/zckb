// Type declarations for custom elements used in the project

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'iconify-icon'?: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
        icon?: string
        class?: string
      }
    }
  }
}

export {}
