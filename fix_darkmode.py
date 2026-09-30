import os
import re

header_template = '''    <!-- ========== HEADER + NAV ========== -->
    <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-30">
        <div class="max-w-4xl mx-auto px-4">
            <div class="flex items-center justify-between h-16">
                <a href="index.html" class="flex items-center gap-2.5 flex-shrink-0">
                    <div class="w-9 h-9 rounded-lg bg-brand-600 flex items-center justify-center shadow-sm">
                        <svg class="w-4.5 h-4.5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.2" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0 0 12 9.75c-2.551 0-5.056.2-7.5.582V21" />
                        </svg>
                    </div>
                    <span class="text-lg font-bold text-gray-900 dark:text-white hidden sm:inline">Portal Laboral</span>
                </a>
                <nav class="hidden md:flex items-center gap-1">
                    <a href="index.html" class="px-3 py-2 rounded-lg text-sm font-medium {nav1} transition">Finiquito</a>
                    <a href="sueldo-neto.html" class="px-3 py-2 rounded-lg text-sm font-medium {nav2} transition">Sueldo Neto</a>
                    <a href="paro.html" class="px-3 py-2 rounded-lg text-sm font-medium {nav3} transition">Calculadora de Paro</a>
                </nav>

                <!-- Theme toggle -->
                <button id="theme-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg text-sm p-2 transition md:ml-2">
                    <svg id="theme-toggle-dark-icon" class="hidden w-6 h-6 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
                    <svg id="theme-toggle-light-icon" class="hidden w-6 h-6 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
                </button>
                <button id="menu-toggle" class="md:hidden p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition" aria-label="Abrir menu">
                    <svg id="icon-open" class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" /></svg>
                    <svg id="icon-close" class="w-6 h-6 hidden" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" /></svg>
                </button>
            </div>
            <div id="mobile-menu" class="md:hidden pb-3" style="max-height:0;opacity:0;overflow:hidden;transition:max-height .3s ease,opacity .3s ease">
                <nav class="flex flex-col gap-1">
                    <a href="index.html" class="px-3 py-2.5 rounded-lg text-sm font-medium {navm1} transition">Calculadora de Finiquito</a>
                    <a href="sueldo-neto.html" class="px-3 py-2.5 rounded-lg text-sm font-medium {navm2} transition">Sueldo Bruto a Neto</a>
                    <a href="paro.html" class="px-3 py-2.5 rounded-lg text-sm font-medium {navm3} transition">Calculadora de Paro</a>
                </nav>
            </div>
        </div>
    </header>'''

fouc_script = '''    <script>
        if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    </script>
</head>'''

js_logic = '''
        const themeToggleBtn = document.getElementById('theme-toggle');
        const darkIcon = document.getElementById('theme-toggle-dark-icon');
        const lightIcon = document.getElementById('theme-toggle-light-icon');
        
        if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            lightIcon.classList.remove('hidden');
        } else {
            darkIcon.classList.remove('hidden');
        }

        if (themeToggleBtn) {
            themeToggleBtn.addEventListener('click', function() {
                darkIcon.classList.toggle('hidden');
                lightIcon.classList.toggle('hidden');
                if (document.documentElement.classList.contains('dark')) {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('theme', 'light');
                } else {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('theme', 'dark');
                }
            });
        }
    })();
    </script>'''

active_class = 'text-brand-700 bg-brand-50 border border-brand-200'
inactive_class = 'text-gray-600 dark:text-gray-400 hover:text-brand-700 hover:bg-brand-50 dark:hover:bg-gray-800'
inactive_class_m = 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'

files = ['sueldo-neto.html', 'paro.html']

for i, file in enumerate(files):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if "darkMode: 'class'" not in content:
        content = re.sub(r'tailwind\.config = \{', "tailwind.config = {\n            darkMode: 'class',", content, count=1)

    if "document.documentElement.classList.add('dark')" not in content:
        content = content.replace("</head>", fouc_script)

    if file == 'sueldo-neto.html':
        h = header_template.format(nav1=inactive_class, nav2=active_class, nav3=inactive_class, navm1=inactive_class_m, navm2=active_class, navm3=inactive_class_m)
    else:
        h = header_template.format(nav1=inactive_class, nav2=inactive_class, nav3=active_class, navm1=inactive_class_m, navm2=inactive_class_m, navm3=active_class)
        
    content = re.sub(r'<header.*?</header>', h, content, flags=re.DOTALL)
    
    # Body fixes
    content = re.sub(r'<body class="([^"]*)"', lambda m: f'<body class="{m.group(1)} dark:bg-gray-900 dark:text-white"'.replace('dark:bg-gray-900 dark:bg-gray-900', 'dark:bg-gray-900').replace('dark:text-white dark:text-white', 'dark:text-white'), content)
    
    if "themeToggleBtn.addEventListener" not in content:
        content = content.replace("})();\n    </script>", js_logic)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fix completed.")
