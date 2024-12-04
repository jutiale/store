// // import Vue from 'vue'
// // import { Router } from 'vue-router'
// import { createMemoryHistory, createRouter } from 'vue-router'

// import Goods from './views/Goods.vue'
// import Categories from './views/Categories.vue'


// const routes = [
//     {
//         path: '/',
//         name: 'goods',
//         component: Goods
//       },
//       {
//         path: '/categories',
//         name: 'categories',
//         component: Categories
//       }
// ];

// const router = createRouter({
//     history: createMemoryHistory(),
//     routes,
//   })

// // export default new Router({
// //   mode: 'history',
// //   base: process.env.BASE_URL,
// //   routes: [
// //     {
// //       path: '/',
// //       name: 'goods',
// //       component: Goods
// //     },
// //     {
// //       path: '/categories',
// //       name: 'categories',
// //       component: Categories
// //     }

// //   ]
// // })
import { createRouter, createWebHistory } from 'vue-router';
import Goods from './views/Goods.vue';
import Categories from './views/Categories.vue';
import Brands from './views/Brands.vue';
import Login from './views/Login.vue'
import GoodRead from './views/GoodRead.vue'
import Users from './views/Users.vue'
import Cart from './views/Cart.vue'
import { authenticationService } from './services/authenticationService';




export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Goods
    },
    {
      path: '/categories',
      name: 'Categories',
      component: Categories
    },
    {
      path: '/goods',
      name: 'Goods',
      component: Goods
    },
    {
      path: '/brands',
      name: 'Brands',
      component: Brands,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/goods/:id',
      name: 'GoodRead',
      component: GoodRead,
    },
    {
      path: '/users',
      name: 'Users',
      component: Users,
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart,
      meta: {
        requiresAuth: true
      }
    },


  ]
});

// router.beforeEach((to, from, next) => {
//   // redirect to login page if not logged in and trying to access a restricted page
//   const { authorize } = to.meta;

//   if (authorize) {
//     const currentUser = authenticationService.currentUserValue;
//     if (!currentUser) {
//       // not logged in so redirect to login page with the return url
//       return next({ path: '/login', query: { returnUrl: to.path } });
//     }

//     // check if route is restricted by role
//     if (authorize.length && !authorize.includes(currentUser.role)) {
//       // role not authorised so redirect to home page
//       return next({ path: '/' });
//     }
//   }

//   next();
// })

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    const currentUser = authenticationService.getCurrentUser;
    if (!currentUser) {
      next({ name: 'Login' })
    } else {
      next() // go to wherever I'm going
    }
  } else {
    next() // does not require auth, make sure to always call next()!
  }
})
export default router;
