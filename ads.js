/* Estructura común para AdSlot. No carga tecnologías publicitarias. */
(() => {
    'use strict';

    const config = window.TDL_AD_CONFIG;
    if (!config || !config.slots) return;

    const adSlots = Array.from(document.querySelectorAll('[data-ad-slot]'));

    adSlots.forEach((slot) => {
        const placement = slot.dataset.adSlot;
        const placementConfig = config.slots[placement];
        if (!placementConfig) {
            slot.hidden = true;
            return;
        }

        slot.classList.add('ad-slot');
        slot.dataset.adFormat = placementConfig.format;
        slot.dataset.adState = 'placeholder';
        slot.dataset.adConsent = 'unknown';
        slot.style.setProperty('--ad-slot-mobile-height', `${placementConfig.mobileHeight}px`);
        slot.style.setProperty('--ad-slot-desktop-height', `${placementConfig.desktopHeight}px`);
        slot.setAttribute('aria-label', 'Publicidad');
        slot.innerHTML = '<span class="ad-slot__label">Publicidad</span><span class="ad-slot__message">Espacio reservado para publicidad</span>';
    });

    function setSlotState(placement, state) {
        if (!['placeholder', 'loading', 'filled', 'disabled-by-consent', 'awaiting-configuration'].includes(state)) return;
        const slot = adSlots.find((item) => item.dataset.adSlot === placement);
        if (!slot || slot.hidden) return;
        slot.dataset.adState = state;
        slot.setAttribute('aria-busy', String(state === 'loading'));
    }

    function setAdvertisingConsent(allowed) {
        if (typeof allowed !== 'boolean') return;

        adSlots.forEach((slot) => {
            if (slot.hidden) return;
            slot.dataset.adConsent = allowed ? 'granted' : 'denied';
            setSlotState(slot.dataset.adSlot, allowed ? 'awaiting-configuration' : 'disabled-by-consent');
            const message = slot.querySelector('.ad-slot__message');
            if (message) {
                message.textContent = allowed
                    ? 'Este espacio se podrá activar cuando se configure AdSense.'
                    : 'Espacio desactivado según tus preferencias.';
            }
        });
    }

    // El gestor de consentimiento puede llamar setAdvertisingConsent() o emitir
    // tdl:consent-change con detail.advertising=true/false. No se guarda el permiso aquí.
    window.TDLAds = Object.freeze({ setAdvertisingConsent, setSlotState });
    window.addEventListener(config.consentEvent, (event) => {
        setAdvertisingConsent(event.detail?.advertising);
    });

    const savedPreferences = window.TDLConsent?.getPreferences();
    if (savedPreferences) setAdvertisingConsent(savedPreferences.categories.advertising);
})();
