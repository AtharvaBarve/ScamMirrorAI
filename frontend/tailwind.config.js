/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                display: ['Space Grotesk', 'sans-serif'],
                mono: ['JetBrains Mono', 'monospace'],
            },
            colors: {
                background: '#060611',
                surface: '#111113',
                primary: '#00E5FF',
                'primary-hover': '#00CCE5',
                danger: '#FF4D6D',
                success: '#22C55E',
                warning: '#FFB703',
                border: 'rgba(255, 255, 255, 0.08)',
                muted: '#A1A1AA',
            },
            boxShadow: {
                'glow': '0 0 20px rgba(0, 229, 255, 0.15)',
                'glow-danger': '0 0 20px rgba(255, 77, 109, 0.15)',
                'card': '0 4px 20px rgba(0, 0, 0, 0.4)',
            }
        },
    },
    plugins: [],
}