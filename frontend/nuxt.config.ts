// https://nuxt.com/docs/api/configuration/nuxt-config

import { definePreset, palette } from "@primeuix/themes";
import Aura from "@primeuix/themes/aura";

export default defineNuxtConfig({
    compatibilityDate: "2025-07-15",
    devtools: { enabled: true },
    modules: [
        "@nuxt/eslint",
        "@nuxt/fonts",
        "@nuxt/image",
        "@primevue/nuxt-module",
        "@nuxt/icon",
    ],

    fonts: {
        defaults: { weights: [400, 700], styles: ["normal", "italic"] },
        families: [{ name: "Pretendard", provider: "local" }],
    },

    primevue: {
        components: {
            prefix: "Pv",
            exclude: ["Form", "FormField"],
        },
        options: {
            theme: {
                preset: definePreset(Aura, {
                    semantic: {
                        primary: palette("#4393e6"),
                        secondary: palette("#eaa248"),
                    },
                }),
            },
        },
    },
});
