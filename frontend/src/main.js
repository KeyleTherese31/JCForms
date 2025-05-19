import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Pages
import WelcomePage from './views/WelcomePage.vue';
import LoginPage from './views/LoginPage.vue';
import RegisterPage from './views/RegisterPage.vue';
import DashboardPage from './views/DashboardPage.vue';

// Components
import AdminSettings from './components/AdminSettings.vue';
import TestsLists from './components/TestsLists.vue';
import JobseekerAnswers from './components/JobseekerAnswers.vue';
import CVEntries from './components/CVEntries.vue';
import CVPreview from './components/CVPreview.vue';

// Superadmin-only (Create this component!)
import AdminPanel from './components/AdminPanel.vue';
import ManageTest from './components/ManageTest.vue';

const routes = [
  { path: '/', component: WelcomePage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { 
    path: '/dashboard', 
    component: DashboardPage,
    meta: { requiresAuth: true }
  },
  { 
    path: '/answers', 
    component: JobseekerAnswers,
    meta: { requiresAuth: true }
  },
  { 
    path: '/cvforms', 
    component: CVEntries,
    meta: { requiresAuth: true }
  },
  { 
    path: '/settings', 
    component: AdminSettings,
    meta: { requiresAuth: true }
  },
  { 
    path: '/tests', 
    component: TestsLists,
    meta: { requiresAuth: true }
  },
  {
    path: '/preview-cv/:id',
    name: 'PreviewCV',
    component: CVPreview,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/adminpanel',
    component: AdminPanel,
    meta: { requiresAuth: true, requiresSuperadmin: true }
  },
  {
    path: '/testpanel',
    component: ManageTest,
    meta: { requiresAuth: true, requiresSuperadmin: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Navigation guard
router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem('access_token');
  const role = localStorage.getItem('admin_role');

  if (to.meta.requiresAuth && !accessToken) {
    // Not logged in
    return next('/login');
  }

  if (to.meta.requiresSuperadmin && role !== 'superadmin') {
    // Logged in but not superadmin
    return next('/dashboard');
  }

  next();
});

createApp(App).use(router).mount('#app');
