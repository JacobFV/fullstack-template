# GOTCHA - Graphical Online Turing test to Confirm Human Activity

## Tech Stack

- Frontend: Vite web app, React with TypeScript for development, TanStack state management and routing, styled with Chakra.

- Backend: FastAPI + Uvicorn server. CRUD, video streaming, authentication and authorization, SQLModel ORM, retry and validation, and more.

## Pages

Auth:

- Login
- Register
- Forgot Password
- Reset Password


Account:

- Verify Email
- Playground
  - interactive test environment
  - get api keys
  - sidebar shows of activity
- Activity
  - all verification
- Billing
  - history
  - projections
- API Keys
  - list of keys
  - expands to show all api key uses for each key
- Settings
  - change name
  - change email
  - change password
  - export data
  - delete account

Verification:

- Verification Request
  - this is the page the use lands on when the system requests verification
  - the user can choose to verify or decline
  - if the user chooses to verify, the system will send the user to the verification page

Public:

- Landing (index)
  - try out our embedded verf gotcha system on the top of the homepage
  - 3 features tailored to our audience
  - pricing
  - contact us (lead funnel)
  - footer (copyright, company name, socials, privacy policy, ToS, etc)
- Privacy Policy
- Terms of Service

Documentation:

- Concepts
- API Reference
- Tutorial
- Contribute
