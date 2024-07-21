import React from 'react';
import { Typography, Box, Link, Paper } from '@mui/material';

export default function AboutPage() {
  return (
    <>
      <Box
        sx={{
          py: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography variant="h1" sx={{ m: 1, mb: 2 }}>
          About page
        </Typography>
        <Box sx={{ mb: 1 }}>
          <Typography variant="body1" display="inline">
            Developer:{' '}
          </Typography>
          <Typography variant="body2" display="inline">
            Edward Birdsall
          </Typography>
        </Box>
        <Typography variant="body1" sx={{ mb: 1 }}>
          LinkedIn
        </Typography>
        <Typography variant="body1" sx={{ mb: 1 }}>
          github:{' '}
          <Link
            href="https://github.com/edward-b-1"
            variant="body2"
            underline="hover"
          >
            edward-b-1
          </Link>
        </Typography>
        <Typography variant="body1" sx={{ mb: 1 }}>
          github:{' '}
          <Link
            href="https://github.com/edbird"
            variant="body2"
            underline="hover"
          >
            edbird
          </Link>
        </Typography>
      </Box>
      <Box
        sx={{
          py: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper sx={{ backgroundColor: 'background.whitesmoke', maxWidth: 0.9 }}>
          <Box sx={{ m: 4 }}>
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <Typography variant="h4" sx={{ mb: 4 }}>
                Story time
              </Typography>
            </Box>
            <Typography variant="body1" sx={{ mb: 1 }}>
              This project initially started during an interview process. I was
              asked to write a Limit Order Book implementation with Python. I
              was given a week to complete the task via Hackerrank.
            </Typography>
            <Typography variant="body1" sx={{ mb: 1 }}>
              I worked on this project during the limited free time that I had
              available. At the time I was working full time for a Hedge Fund. I
              managed to complete most of the task, however my implementation
              failed on some of the test cases. The test inputs and outputs were
              hidden from me, and so I eventually gave up trying to fix a system
              where I had no access to the information which would have enabled
              me to debug the remaining issues. I was not invited to a further
              interview stage.
            </Typography>
            <Typography variant="body1" sx={{ mb: 1 }}>
              I realized that what I had produced would make a good project for
              my portfolio, and so I uploaded my work to github. During the
              development process, I also realized that the implementation could
              be improved significiantly, and so I then re-wrote the
              implementation.
            </Typography>
            <Typography variant="body1" sx={{ mb: 1 }}>
              Having completed this, I figured that it would be quite a nice
              extension to wrap the business logic of the Limit Order Book
              behind a REST API webserver, which would also allow others to not
              only read my code on github but also interact with it. So I
              implemented a backend webserver with Python and FastAPI. I then
              deployed the application to the cloud.
            </Typography>
            <Typography variant="body1" sx={{ mb: 1 }}>
              I then wrote a command line interface, again using Python, which
              could be downloaded and run by anyone who wanted to interact with
              the REST API.
            </Typography>
            <Typography variant="body1" sx={{ mb: 1 }}>
              I sent information about how to use my application as part of my
              application to a number of roles. It then became apparent to me
              that interfacing with a REST API directly was too unfamiliar for
              most people. I could tell from the webserver logs that it wasn't
              being used. I sent my work to a few friends of varying technical
              ability and it became apparent that what was needed was a more
              familar web interface.
            </Typography>
            <Typography variant="body1" sx={{ mb: 1 }}>
              The end result is the website which you are using right now. To
              build it, I had to learn React. I learned enough React concepts to
              build this in 1 week. The Limit Order Book implementation took
              about a week to write, and a similar amount of time was required
              to write the FastAPI interface.
            </Typography>
            <Box
              sx={{
                mt: 4,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <Link href="/mainpage" variant="body2" underline="hover">
                go back
              </Link>
            </Box>
          </Box>
        </Paper>
      </Box>
    </>
  );
}
