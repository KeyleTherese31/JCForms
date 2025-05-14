import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Pages
import WelcomePage from './views/WelcomePage.vue';
import LoginPage from './views/LoginPage.vue';
import RegisterPage from './views/RegisterPage.vue';
import DashboardPage from './views/DashboardPage.vue';

// Placeholder components (update these with real ones later)
const TestsPage = { template: '<div><h2>Test & Questions Page</h2></div>' };
const AnswersPage = { template: '<div><h2>Jobseeker\'s Answer Entries</h2></div>' };
const CVFormsPage = { template: '<div><h2>Jobseeker\'s CV Form Entries</h2></div>' };
const SettingsPage = { template: '<div><h2>Settings Page</h2></div>' };

const routes = [
  { path: '/', component: WelcomePage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/dashboard', component: DashboardPage },
  { path: '/tests', component: TestsPage },
  { path: '/answers', component: AnswersPage },
  { path: '/cvforms', component: CVFormsPage },
  { path: '/settings', component: SettingsPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount('#app');
