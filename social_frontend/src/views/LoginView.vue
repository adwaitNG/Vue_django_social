<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Log In</h1>
        <p class="mb-6 text-gray-500">
          Have never tried any virual connection? It is recommended for people
          who love to argue but hate to talk! who love to argue but hate to
          talk! who love to argue but hate to talk! who love to argue but hate
          to talk!who love to argue but hate to talk! who love to argue but hate
          to talk!
        </p>
        <p class="font-bold">
          Dont have an account?
          <router-link :to="{ name: 'sigup' }" class="underline"
            >click here</router-link
          >
          to Sign up!!
        </p>
      </div>
    </div>
    <div class="mian-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6">
          <div>
            <label>E-mail</label><br />
            <input
              type="email"
              placeholder="Your e-mail address"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <label>Password</label><br />
            <input
              type="password"
              placeholder="Your password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">
              Login In
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
