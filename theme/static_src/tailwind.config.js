/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                "primary": "#ee7e25",
                "primary-light": "#ffb057",
                'secondary-light': '#bac5b9',
                'secondary': '#032900',
                'secondary-dark': '#051900',
                "neutral": "#23282F",
                "info": "#90cbd4",
                "success": "#6CB288",
                "warning": "#fdcb10",
                "error": "#fc483f",
                'facebook': '#3b5998',
                'whatsapp': '#25d366'
            },
            height: {
                'screen75': '75vh',
                'screen80': '80vh',
            },
            dropShadow: {
                'black': '0px 0px 6px black',
            },
            fontFamily: {
                'specialElite': ['Special Elite', 'cursive'],
                'SecularOne': ['Secular One', 'sans-serif']
              },
            animation: {
                "fade-in-fwd": "fade-in-fwd 4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both",
            },
            keyframes: {
                "fade-in-fwd": {
                    "0%": {                        
                        opacity: "0"
                    },
                    to: {                        
                        opacity: "1"
                    }
                },
            },
        },
    },
    plugins: [
        // require('@tailwindcss/aspect-ratio'),
        // require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        // require('@tailwindcss/line-clamp'),
    ],
}
