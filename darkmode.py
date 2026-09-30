import os
import re

files = ['index.html', 'sueldo-neto.html', 'paro.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Tailwind Config
    if "darkMode: 'class'" not in content:
        content = re.sub(r'tailwind\.config = \{', "tailwind.config = {\n            darkMode: 'class',", content, count=1)
    
    # 2. FOUC Script in head
    fouc_script = '''    <script>
        if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    </script>
</head>'''
    if "document.documentElement.classList.add('dark')" not in content:
        content = content.replace("</head>", fouc_script)

    # 3. Toggle Button next to hamburger
    toggle_btn = '''
                <!-- Theme toggle -->
                <button id="theme-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg text-sm p-2 transition md:ml-2">
                    <svg id="theme-toggle-dark-icon" class="hidden w-6 h-6 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
                    <svg id="theme-toggle-light-icon" class="hidden w-6 h-6 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
                </button>
                <button id="menu-toggle"'''
    
    if 'id="theme-toggle"' not in content:
        content = re.sub(r'<\/nav>\s*<button id="menu-toggle"', "</nav>\n" + toggle_btn, content)

    # 4. Global Dark Mode Classes
    def add_dark_classes(match):
        cls = match.group(1)
        
        # Text colors
        cls = re.sub(r'\btext-gray-900\b', 'text-gray-900 dark:text-white', cls)
        cls = re.sub(r'\btext-gray-800\b', 'text-gray-800 dark:text-gray-200', cls)
        cls = re.sub(r'\btext-gray-700\b', 'text-gray-700 dark:text-gray-300', cls)
        cls = re.sub(r'\btext-gray-600\b', 'text-gray-600 dark:text-gray-400', cls)
        cls = re.sub(r'\btext-gray-500\b', 'text-gray-500 dark:text-gray-400', cls)
        cls = re.sub(r'\btext-gray-400\b', 'text-gray-400 dark:text-gray-500', cls)
        
        # Backgrounds & Borders
        cls = re.sub(r'\bbg-white\b', 'bg-white dark:bg-gray-800', cls)
        cls = re.sub(r'\bbg-gray-50\b', 'bg-gray-50 dark:bg-gray-900', cls)
        cls = re.sub(r'\bborder-gray-200\b', 'border-gray-200 dark:border-gray-700', cls)
        cls = re.sub(r'\bborder-gray-300\b', 'border-gray-300 dark:border-gray-600', cls)
        cls = re.sub(r'\bborder-gray-100\b', 'border-gray-100 dark:border-gray-700', cls)
        
        # Ensure inputs/selects get dark background and text
        if 'border-gray-300' in cls and ('px-4' in cls or 'pl-8' in cls): 
            if 'dark:bg-gray-700' not in cls:
                cls += ' dark:bg-gray-700 dark:text-white'
                
        # Fix duplicate darks if any
        cls = ' '.join(list(dict.fromkeys(cls.split())))
        
        return f'class="{cls}"'

    content = re.sub(r'class="([^"]+)"', add_dark_classes, content)

    # 5. JS Logic
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
    
    if "themeToggleBtn.addEventListener" not in content:
        content = content.replace("})();\n    </script>", js_logic)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Modo oscuro aplicado a todos los archivos.")
