import { createRouter, createWebHistory } from 'vue-router';
import JobseekerLogin from '@/views/JobseekerLogin.vue';
import CVForm from '@/views/CVForm.vue';
import MobileLogin from '@/views/MobileLogin.vue';

const routes = [
  { path: '/', component: JobseekerLogin },
  { path: '/cv-form', component: CVForm },
  { path: '/mobile-login', component: MobileLogin },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
