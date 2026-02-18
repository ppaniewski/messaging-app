import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react"

const config = defineConfig({
    theme: {
        semanticTokens: {
            colors: {
                midBg: {
                    value: { base: "{colors.blackAlpha.200}", _dark: "{colors.whiteAlpha.200}" }
                },
                slightBg: {
                    value: { base: "{colors.blackAlpha.100}", _dark: "{colors.whiteAlpha.50}" }
                }
            }
        }
    }
})

export default createSystem(defaultConfig, config)