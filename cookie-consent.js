/* Consentimiento local por categorías. No integra proveedores de terceros. */
(() => {
    'use strict';

    const CONSENT_VERSION = 1;
    const STORAGE_KEY = 'tdl_cookie_consent';
    const CONSENT_MAX_AGE_MS = 730 * 24 * 60 * 60 * 1000;
    const OPTIONAL_CATEGORIES = ['preferences', 'analytics', 'advertising'];
    const validCategories = (categories) => categories
        && categories.necessary === true
        && OPTIONAL_CATEGORIES.every((category) => typeof categories[category] === 'boolean');

    function readStoredConsent() {
        try {
            const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
            const age = Date.now() - saved?.updatedAt;
            return saved?.version === CONSENT_VERSION
                && Number.isFinite(saved.updatedAt)
                && age >= 0 && age < CONSENT_MAX_AGE_MS
                && validCategories(saved.categories) ? saved : null;
        } catch {
            return null;
        }
    }

    let preferences = readStoredConsent();
    let openPreferencesHandler = () => {};

    // La preferencia visual anterior a este panel no se lee ni conserva sin permiso.
    if (!preferences?.categories.preferences) {
        try { localStorage.removeItem('theme'); } catch { /* almacenamiento no disponible */ }
    }

    function announceChange() {
        window.dispatchEvent(new CustomEvent('tdl:consent-change', {
            detail: {
                version: CONSENT_VERSION,
                necessary: true,
                preferences: preferences.categories.preferences,
                analytics: preferences.categories.analytics,
                advertising: preferences.categories.advertising
            }
        }));
    }

    const consentApi = {
        version: CONSENT_VERSION,
        getPreferences: () => preferences ? JSON.parse(JSON.stringify(preferences)) : null,
        hasConsent: (category) => category === 'necessary' || Boolean(preferences?.categories[category]),
        getPreference: (key) => {
            if (key !== 'theme' || !consentApi.hasConsent('preferences')) return null;
            try { return localStorage.getItem('theme'); } catch { return null; }
        },
        setPreference: (key, value) => {
            if (key !== 'theme' || !consentApi.hasConsent('preferences') || !['dark', 'light'].includes(value)) return false;
            try { localStorage.setItem('theme', value); return true; } catch { return false; }
        },
        openPreferences: () => openPreferencesHandler(document.activeElement)
    };
    window.TDLConsent = Object.freeze(consentApi);

    if (preferences) announceChange();

    function saveCategories(categories) {
        const next = {
            version: CONSENT_VERSION,
            updatedAt: Date.now(),
            categories: {
                necessary: true,
                preferences: categories.preferences === true,
                analytics: categories.analytics === true,
                advertising: categories.advertising === true
            }
        };

        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
        } catch {
            // La decisión se aplica durante esta visita aunque el navegador bloquee el almacenamiento.
        }

        preferences = next;
        if (!next.categories.preferences) {
            try { localStorage.removeItem('theme'); } catch { /* almacenamiento no disponible */ }
        }
        announceChange();
        return next;
    }

    function buildInterface() {
        const banner = document.createElement('section');
        banner.className = 'cookie-banner';
        banner.id = 'tdl-cookie-banner';
        banner.setAttribute('aria-labelledby', 'tdl-cookie-banner-title');
        banner.setAttribute('aria-describedby', 'tdl-cookie-banner-copy');
        banner.hidden = Boolean(preferences);
        banner.innerHTML = `
            <div class="cookie-banner__copy">
                <strong id="tdl-cookie-banner-title">Tu privacidad importa</strong>
                <p id="tdl-cookie-banner-copy">Usamos almacenamiento necesario para recordar tu elección. Las preferencias, analítica y publicidad opcionales solo se activan si las autorizas. <a href="${location.pathname.endsWith('/legales.html') || location.pathname.endsWith('legales.html') ? '#cookies' : 'legales.html#cookies'}">Política de Cookies</a>.</p>
            </div>
            <div class="cookie-banner__actions">
                <button type="button" class="cookie-button cookie-button--primary" data-cookie-action="accept">Aceptar todas</button>
                <button type="button" class="cookie-button cookie-button--primary" data-cookie-action="reject">Rechazar todas</button>
                <button type="button" class="cookie-button" data-cookie-action="configure">Configurar cookies</button>
            </div>`;

        const dialog = document.createElement('dialog');
        dialog.className = 'cookie-dialog';
        dialog.id = 'tdl-cookie-dialog';
        dialog.setAttribute('aria-labelledby', 'tdl-cookie-dialog-title');
        dialog.innerHTML = `
            <div class="cookie-dialog__header">
                <div><p class="cookie-dialog__eyebrow">TuDineroLaboral</p><h2 id="tdl-cookie-dialog-title">Preferencias de cookies</h2></div>
                <button type="button" class="cookie-dialog__close" data-cookie-action="close" aria-label="Cerrar sin guardar">×</button>
            </div>
            <p class="cookie-dialog__intro">Elige qué categorías opcionales permites. Puedes cambiar o retirar tu elección cuando quieras desde el enlace «Configurar cookies» del pie de página.</p>
            <div class="cookie-category cookie-category--required">
                <div><h3>Necesarias</h3><p>Permiten guardar y aplicar tu elección y mantener las funciones básicas del sitio.</p></div>
                <label class="cookie-toggle"><span class="cookie-toggle__text">Siempre activas</span><input type="checkbox" role="switch" checked disabled aria-label="Cookies necesarias, siempre activas"></label>
            </div>
            <div class="cookie-category">
                <div><h3>Preferencias</h3><p>Permiten recordar opciones como el tema claro u oscuro.</p></div>
                <label class="cookie-toggle"><span class="cookie-toggle__text">Permitir</span><input type="checkbox" role="switch" data-cookie-category="preferences" aria-label="Permitir preferencias"></label>
            </div>
            <div class="cookie-category">
                <div><h3>Analíticas</h3><p>Ayudarían a medir el uso del sitio. Actualmente no hay herramientas analíticas integradas.</p></div>
                <label class="cookie-toggle"><span class="cookie-toggle__text">Permitir</span><input type="checkbox" role="switch" data-cookie-category="analytics" aria-label="Permitir analíticas"></label>
            </div>
            <div class="cookie-category">
                <div><h3>Publicidad</h3><p>Reservada para publicidad y su medición. AdSense aún no está integrado y no se cargará por esta elección sola.</p></div>
                <label class="cookie-toggle"><span class="cookie-toggle__text">Permitir</span><input type="checkbox" role="switch" data-cookie-category="advertising" aria-label="Permitir publicidad"></label>
            </div>
            <p class="cookie-dialog__error" role="status" aria-live="polite" hidden></p>
            <div class="cookie-dialog__actions">
                <button type="button" class="cookie-button" data-cookie-action="close">Cerrar sin guardar</button>
                <button type="button" class="cookie-button cookie-button--text" data-cookie-action="withdraw">Retirar consentimiento</button>
                <button type="button" class="cookie-button cookie-button--primary" data-cookie-action="save">Guardar selección</button>
            </div>
            <p class="cookie-dialog__policy">Más información en la <a href="${location.pathname.endsWith('legales.html') ? '#cookies' : 'legales.html#cookies'}">Política de Cookies</a>.</p>`;

        document.body.append(banner, dialog);
        let returnFocus = null;

        function closeDialog() {
            if (dialog.open) dialog.close();
        }

        function openDialog(trigger) {
            if (!dialog.isConnected) return;
            returnFocus = trigger instanceof HTMLElement ? trigger : document.activeElement;
            const current = preferences?.categories;
            dialog.querySelectorAll('[data-cookie-category]').forEach((input) => {
                input.checked = current ? current[input.dataset.cookieCategory] === true : false;
            });
            const error = dialog.querySelector('.cookie-dialog__error');
            error.hidden = true;
            error.textContent = '';
            if (!dialog.open) dialog.showModal();
            dialog.querySelector('[data-cookie-action="save"]').focus();
        }

        function finishDialog() {
            if (returnFocus instanceof HTMLElement && returnFocus.isConnected && !returnFocus.closest('[hidden]')) {
                returnFocus.focus();
            } else {
                document.querySelector('[data-cookie-open]')?.focus();
            }
        }

        function commit(categories) {
            saveCategories(categories);
            banner.hidden = true;
            closeDialog();
            finishDialog();
        }

        banner.addEventListener('click', (event) => {
            const button = event.target.closest('[data-cookie-action]');
            if (!button) return;
            if (button.dataset.cookieAction === 'accept') {
                commit({ preferences: true, analytics: true, advertising: true });
            } else if (button.dataset.cookieAction === 'reject') {
                commit({ preferences: false, analytics: false, advertising: false });
            } else if (button.dataset.cookieAction === 'configure') {
                openDialog(button);
            }
        });

        dialog.addEventListener('click', (event) => {
            const button = event.target.closest('[data-cookie-action]');
            if (!button) return;
            const action = button.dataset.cookieAction;
            if (action === 'close') {
                closeDialog();
                finishDialog();
            } else if (action === 'save' || action === 'withdraw') {
                const categories = action === 'withdraw'
                    ? { preferences: false, analytics: false, advertising: false }
                    : Object.fromEntries(OPTIONAL_CATEGORIES.map((category) => [
                        category,
                        dialog.querySelector(`[data-cookie-category="${category}"]`).checked
                    ]));
                commit(categories);
            }
        });

        dialog.addEventListener('cancel', (event) => {
            event.preventDefault();
            closeDialog();
            finishDialog();
        });
        dialog.addEventListener('close', finishDialog);
        document.addEventListener('click', (event) => {
            const trigger = event.target.closest('[data-cookie-open]');
            if (trigger) openDialog(trigger);
        });

        openPreferencesHandler = openDialog;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildInterface, { once: true });
    } else {
        buildInterface();
    }
})();
