
import { createTheme } from '@mui/material/styles';

const marineBlue = "#013E87";
const berkeleyBlue = "#002b5e";
const whiteSmoke = "#f5f5f5";
const whiteSmokeDark = "#ebebeb";
const eerieBlack = "#222725";
const orangePeel = "#ff9f1c";
const textfieldBackgroundColor = "#dddddd";
const taupeGray = "#999799";

export const globalTheme = createTheme({
  typography: {
    body1: {
      fontWeight: 400,
      fontSize: '1.0rem',
    },
    body2: {
      fontWeight: 500,
      fontSize: '1.0rem',
    },
    button: {
      fontWeight: 500,
      fontSize: '1.0rem',
      textTransform: '',
    },
    caption: {

    },
    overline: {

    },
    h1: {
      fontSize: '3rem',
      fontWeight: 400,
    },
    h2: {
      fontSize: '2rem',
    },
    h3: {
      fontSize: '2rem',
    },
    h4: {
      fontSize: '1.75rem',
    },
    h5: {
      fontSie: '1.5rem',
    },
    h6: {
      fontSize: '1.3rem',
    },
    subtitle1: {

    },
    subtitle2: undefined,
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
  },

  palette: {
    primary: {
      main: "#013e87",
    },
    text: {
      primary: eerieBlack,
      secondary: "#002b5e",
      disabled: "#131615",
    },
    common: {
      white: taupeGray,
      black: eerieBlack,
    },
    background: {
      whitesmoke: whiteSmoke,
      default: "#EBEAEB",
      paper: "#ffffff",
    },
    marineBlue: marineBlue,
    berkeleyBlue: berkeleyBlue,
    whiteSmoke: whiteSmoke,
    eerieBlack: eerieBlack,
    orangePeel: orangePeel,
    textfieldBackgroundColor: textfieldBackgroundColor,
  },

  // palette: {
  //   // antiflashWhite: theme.palette.augmentColor({
  //   //   color: {
  //   //     main: '#EBEAEB',
  //   //   },
  //   //   name: 'antiflashWhite',
  //   // }),
  //   primary: {
  //     main: "#2541B2",
  //     contrastText: "#EBEAEB",
  //   },
  //   secondary: {
  //     main: "#222725",
  //   },
  //   error: {
  //     main: "#D81E5B",
  //   },
  //   text: {
  //     primary: "#222725",
  //     secondary: "#0D6D6A",
  //     disabled: "#131615",
  //   },
  //   common: {
  //     white: "#999799",
  //     black: "#222725",
  //   },
  //   background: {
  //     whitesmoke: "#F5F5F5",
  //     default: "#EBEAEB",
  //     paper: "#ffffff",
  //   },
  //   taupeGray: "#999799",
  //   perisanBlue: "#2541B2",
  //   eerieBlack: "#222725",
  //   raspberry: "#D81E5B",
  //   caribbeanCurrent: "#0D6D6A",
  //   caribbeanCurrentDark: "#0B5B59",
  //   verdigris: "#17BEBB",
  //   night: "#131615",
  //   silver: "#C2C1C2",
  //   antiflashWhite: "#EBEAEB",
  //   whiteSmoke: "#F5F5F5",
  //   textfieldBackgroundColor: "#dddddd",
  // }

  components: {
    MuiButtonBase: {
      defaultProps: {
        disableRipple: true,
      }
    },
    MuiAccordion: {
      styleOverrides: {
        root: {
          backgroundColor: whiteSmoke,
          borderRadius: "8px",
          '&:before': {
            display: "none",
          },
          '&.Mui-expanded': {
            // borderTop: "8px",
            // borderBottom: "0px",
            borderRadius: '8px',
          }
        },
        // expanded: {
        //   borderRadius: "8px",
        // },
      }
    },
    MuiAccordionSummary: {
      styleOverrides: {
        root: {
          backgroundColor: whiteSmokeDark,
          // borderRadius: "8px",
          borderTopLeftRadius: "8px",
          borderTopRightRadius: "8px",
          borderBottomLeftRadius: "8px",
          borderBottomRightRadius: "8px",
          '&.Mui-expanded': {
            backgroundColor: whiteSmoke,
            //borderTop: "8px",
            borderBottom: "none",
            borderBottomLeftRadius: "0px",
            borderBottomRightRadius: "0px",
          }
        },
        // expanded: {
        //   borderTop: "8px",
        // },
        content: {
          fontWeight: 'bold',
        }
      }
    },
    MuiAccordionDetails: {
      styleOverrides: {
        root: {
          // borderRadius: "8px",
          borderBottomLeftRadius: "8px",
          borderBottomRightRadius: "8px",
        }
      }
    }
  }
});


