<template>
    <div class="flex justify-center items-center h-screen">
      <form @submit="" class="p-6 bg-transparent rounded-full"> <!--insert @submit="" before class-->
        <div class="mb-6">
			<img src="/assets/img/logo/gl_logo.png" alt="logo" class="mx-auto"/>
		</div>
        <h2 class="mb-6 tracking-wide leading-tight font-black text-5xl text-center">Verify your email</h2>
        <div class="mb-14 font-bold tracking-wide text-center">
          <label for="code" class=" mb-6 text-lg font-light text-5">
            We've sent a verification code to your email <br>=youremail@email.com
          </label>
          <input type="text" id="code" name="code" v-model="code" placeholder="enter verification code" class="my-5 bg-transparent w-2/3 py-3 px-6 border border-purple1 rounded-full"
          />
          <!-- insert v-model="" under name="" -->
        </div>
        <div class="space-y-2 text-center">
            <button type="button" @click="handleBack" class="active:bg-purple_main inline-block text-center w-24 p-2 bg-[#8250CB] text-white rounded-full">Back</button>
            <button type="submit" class="active:bg-purple_main ml-7 inline-block text-center w-24 p-2 bg-[#8250CB] text-white rounded-full">Verify</button>
        </div>
      </form>
    </div>
  </template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const code = ref("");

    const handleSubmit = (e) => {
      e.preventDefault();
      // Handle form submission logic here
      console.log('Verification code:', code.value);
    };

    const handleBack = () => {
      // Handle back button logic here
      console.log('Go back');
    };

    return {
      code,
      handleSubmit,
      handleBack
    };
  },
};
</script>

