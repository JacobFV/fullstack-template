import { extendTheme } from "@chakra-ui/react"

const disabledStyles = {
  _disabled: {
    backgroundColor: "ui.main",
  },
}

// export const THEME_COLORS = {
//   PRIMARY: "#0077ff",
//   SECONDARY: "#ff9900",
//   SUCCESS: "#00cc00",
//   ERROR: "#ff0000",
//   WARNING: "#ffcc00",
//   INFO: "#0099ff",
// };

// export const THEME_FONTS = {
//   HEADING: "Inter, sans-serif",
//   BODY: "Inter, sans-serif",
// };

// export const THEME_BREAKPOINTS = {
//   SM: "30em",
//   MD: "48em",
//   LG: "62em",
//   XL: "80em",
//   "2XL": "96em",
// };


const theme = extendTheme({
  colors: {
    ui: {
      main: "#009688",
      secondary: "#EDF2F7",
      success: "#48BB78",
      danger: "#E53E3E",
      light: "#FAFAFA",
      dark: "#1A202C",
      darkSlate: "#252D3D",
      dim: "#A0AEC0",
    },
  },
  components: {
    Button: {
      variants: {
        primary: {
          backgroundColor: "ui.main",
          color: "ui.light",
          _hover: {
            backgroundColor: "#00766C",
          },
          _disabled: {
            ...disabledStyles,
            _hover: {
              ...disabledStyles,
            },
          },
        },
        danger: {
          backgroundColor: "ui.danger",
          color: "ui.light",
          _hover: {
            backgroundColor: "#E32727",
          },
        },
      },
    },
    Tabs: {
      variants: {
        enclosed: {
          tab: {
            _selected: {
              color: "ui.main",
            },
          },
        },
      },
    },
  },
})

export default theme
