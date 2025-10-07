# 🎨 Frontend - HRGSMS React Application

Modern, responsive frontend for the Hotel Reservation and Guest Services Management System built with React 19, TypeScript, and Vite.

## 📋 Overview

The HRGSMS frontend is a single-page application (SPA) that provides an intuitive interface for hotel staff to manage reservations, guests, rooms, and billing across multiple hotel branches.

## 🛠️ Tech Stack

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 7.1.7
- **Styling**: Tailwind CSS 3.4.18
- **Icons**: Lucide React 0.544.0
- **HTTP Client**: Axios 1.12.2
- **Routing**: React Router DOM 7.9.3
- **Notifications**: React Toastify 11.0.5
- **Date Handling**: date-fns 4.1.0
- **Code Quality**: ESLint + TypeScript ESLint

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn package manager

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

### Development Server

- **URL**: http://localhost:5173
- **Hot Reload**: Enabled
- **TypeScript**: Full support with type checking

## 📁 Project Structure

```
frontend/
├── 📄 package.json              # Dependencies and scripts
├── 📄 vite.config.ts            # Vite configuration
├── 📄 tailwind.config.js        # Tailwind CSS configuration
├── 📄 tsconfig.json             # TypeScript configuration
├── 📄 eslint.config.js          # ESLint configuration
├── 📄 postcss.config.js         # PostCSS configuration
├── 📄 index.html               # Main HTML template
└── 📂 src/                     # Source code
    ├── 🎯 main.tsx             # Application entry point
    ├── 📱 App.tsx              # Main app component
    ├── 🎨 App.css              # Global app styles
    ├── 🎨 index.css            # Global CSS with Tailwind
    ├── 📂 components/          # Reusable UI components
    │   ├── 📂 auth/           # Authentication components
    │   ├── 📂 common/         # Common UI components
    │   └── 📂 layout/         # Layout components
    ├── 📂 pages/              # Page components
    │   ├── 🏠 DashboardPage.tsx
    │   ├── 🏨 RoomsPage.tsx
    │   ├── 📅 ReservationsPage.tsx
    │   ├── 👥 GuestsPage.tsx
    │   ├── 🛎️ ServicesPage.tsx
    │   ├── 💰 BillingPage.tsx
    │   ├── 📊 ReportsPage.tsx
    │   └── 📄 index.ts
    ├── 📂 services/           # API service functions
    │   ├── 🌐 api.ts          # Base API configuration
    │   ├── 🔐 authService.ts  # Authentication services
    │   ├── 🏨 roomService.ts  # Room management
    │   ├── 📅 bookingService.ts # Booking operations
    │   ├── 👥 guestService.ts # Guest management
    │   ├── 🛎️ serviceService.ts # Hotel services
    │   ├── 💰 billingService.ts # Billing operations
    │   └── 📄 index.ts
    ├── 📂 types/              # TypeScript type definitions
    │   └── 📄 index.ts
    ├── 📂 context/            # React context providers
    │   └── 🔐 AuthContext.tsx # Authentication context
    └── 📂 assets/            # Static assets
        └── 🖼️ react.svg
```

## 🎨 UI Components

### Layout Components

- **Header**: Navigation and user menu
- **Sidebar**: Main navigation menu
- **Footer**: System information and links
- **Layout**: Main page wrapper

### Common Components

- **Button**: Styled button with variants
- **Card**: Content container component
- **Modal**: Overlay dialog component
- **Form**: Input components and validation
- **Table**: Data display with sorting/filtering
- **Loading**: Loading states and spinners

### Feature Components

- **RoomCard**: Room information display
- **ReservationForm**: Booking creation/editing
- **GuestProfile**: Guest information management
- **ServiceRequest**: Service ordering interface
- **BillingSummary**: Payment and billing details

## 📱 Pages

### 🏠 Dashboard

- Overview statistics
- Recent activities
- Quick actions
- Branch performance metrics

### 🏨 Rooms Management

- Room availability overview
- Room type management
- Status updates
- Maintenance scheduling

### 📅 Reservations

- Booking calendar view
- Reservation creation/editing
- Check-in/check-out processes
- Booking history

### 👥 Guests Management

- Guest profiles
- Contact information
- Stay history
- Loyalty program details

### 🛎️ Services

- Available hotel services
- Service requests
- Order management
- Service history

### 💰 Billing

- Invoice generation
- Payment processing
- Billing history
- Revenue reports

### 📊 Reports

- Occupancy reports
- Revenue analytics
- Guest satisfaction
- Operational metrics

## 🔧 Configuration

### Vite Configuration

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
```

### Tailwind CSS

- Custom color palette for hotel branding
- Responsive design utilities
- Component-specific styles
- Dark mode support (planned)

### TypeScript

- Strict type checking enabled
- Path mapping for cleaner imports
- Interface definitions for API responses
- Type-safe routing

## 🌐 API Integration

### Base Configuration

```typescript
const API_BASE_URL = "http://localhost:8000/api";
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});
```

### Authentication

- JWT token management
- Automatic token refresh
- Protected route handling
- Session persistence

### Error Handling

- Global error interceptors
- User-friendly error messages
- Retry mechanisms
- Offline detection

## 🔐 Security

### Authentication Flow

1. Login with credentials
2. Receive JWT token
3. Store token securely
4. Include token in API requests
5. Handle token expiration

### Data Protection

- Input sanitization
- XSS protection
- CSRF prevention
- Secure token storage

## 🎯 State Management

### React Context

- Authentication state
- User preferences
- Theme settings
- Global notifications

### Local State

- Component-specific state
- Form handling
- UI interactions
- Temporary data

## 📱 Responsive Design

### Breakpoints

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### Features

- Mobile-first design approach
- Touch-friendly interfaces
- Adaptive layouts
- Optimized navigation

## 🧪 Development

### Code Quality

- ESLint for code linting
- TypeScript for type safety
- Prettier for code formatting
- Git hooks for quality gates

### Testing Strategy

- Unit tests with Vitest (planned)
- Component testing with React Testing Library
- E2E tests with Playwright (planned)
- Visual regression testing

### Performance

- Code splitting with React.lazy
- Image optimization
- Bundle size monitoring
- Performance metrics tracking

## 🚀 Deployment

### Build Process

```bash
# Production build
npm run build

# Output directory: dist/
# Static files ready for deployment
```

### Environment Variables

```bash
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=HRGSMS
VITE_ENABLE_ANALYTICS=false
```

### Deployment Options

- Static hosting (Vercel, Netlify)
- CDN deployment
- Docker containerization
- CI/CD integration

## 🔧 Customization

### Styling

- Modify `tailwind.config.js` for design system
- Update CSS variables in `index.css`
- Component-specific styles in modules

### Features

- Add new pages in `src/pages/`
- Create components in `src/components/`
- Extend services in `src/services/`

## 🐛 Troubleshooting

### Common Issues

1. **Build Errors**: Check TypeScript types and imports
2. **API Errors**: Verify backend connection and CORS
3. **Style Issues**: Check Tailwind classes and CSS conflicts
4. **Routing Problems**: Verify React Router configuration

### Development Tools

- React Developer Tools
- Vite Inspector
- TypeScript Language Server
- Browser DevTools

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/)

---

**Modern, fast, and user-friendly interface for hotel management** ⚡
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
globalIgnores(['dist']),
{
files: ['**/*.{ts,tsx}'],
extends: [
// Other configs...
// Enable lint rules for React
reactX.configs['recommended-typescript'],
// Enable lint rules for React DOM
reactDom.configs.recommended,
],
languageOptions: {
parserOptions: {
project: ['./tsconfig.node.json', './tsconfig.app.json'],
tsconfigRootDir: import.meta.dirname,
},
// other options...
},
},
])

```

```
