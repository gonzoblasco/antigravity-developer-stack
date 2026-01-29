---
name: nextjs-saas
description: Next.js SaaS template principles. Auth, payments, email.
---

# Next.js SaaS Template

## Tech Stack

| Component | Technology                                      |
| --------- | ----------------------------------------------- |
| Framework | Next.js 16 (App Router)                         |
| Auth      | Auth.js v5                                      |
| Payments  | Stripe                                          |
| Database  | PostgreSQL + Prisma                             |
| Email     | Resend                                          |
| UI        | Tailwind (ASK USER: shadcn/Headless UI/Custom?) |

---

## Directory Structure

```
project-name/
├── prisma/
├── src/
│   ├── app/
│   │   ├── (auth)/      # Login, register
│   │   ├── (dashboard)/ # Protected routes
│   │   ├── (marketing)/ # Landing, pricing
│   │   └── api/
│   │       ├── auth/[...nextauth]/
│   │       └── webhooks/stripe/
│   ├── components/
│   │   ├── auth/
│   │   ├── billing/
│   │   └── dashboard/
│   ├── lib/
│   │   ├── auth.ts      # Auth.js config
│   │   ├── stripe.ts    # Stripe client
│   │   └── email.ts     # Resend client
│   └── config/
│       └── subscriptions.ts
└── package.json
```

---

## SaaS Features

| Feature        | Implementation           |
| -------------- | ------------------------ |
| Auth           | Auth.js + OAuth          |
| Subscriptions  | Stripe Checkout          |
| Billing Portal | Stripe Portal            |
| Webhooks       | Stripe events            |
| Email          | Transactional via Resend |

---

## Database Schema

| Model   | Fields                                      |
| ------- | ------------------------------------------- |
| User    | id, email, stripeCustomerId, subscriptionId |
| Account | OAuth provider data                         |
| Session | User sessions                               |

---

## Environment Variables

| Variable              | Purpose                               |
| --------------------- | ------------------------------------- |
| DATABASE_URL          | Prisma                                |
| NEXTAUTH_SECRET       | Auth                                  |
| STRIPE_SECRET_KEY     | Payments                              |
| STRIPE_WEBHOOK_SECRET | Webhooks                              |
| RESEND_API_KEY        | Email                                 |
| AUTH_SECRET           | Auth secret (legacy: NEXTAUTH_SECRET) |

---

## Setup Steps

1. `npx create-next-app@latest {{name}} --typescript --tailwind --app --turbopack`
2. Install: `npm install next-auth@beta @auth/prisma-adapter stripe resend`
3. Setup Stripe products/prices
4. Configure environment
5. `npm run db:push`
6. `npm run stripe:listen` (webhooks)
7. `npm run dev`

---

## Best Practices

- Route groups for layout separation
- Stripe webhooks for subscription sync
- Auth.js with Prisma adapter
- Email templates with React Email
