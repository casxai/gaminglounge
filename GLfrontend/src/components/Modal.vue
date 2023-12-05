<template>
  
  <transition name="modal=animation">
    <div v-show="modalActive" class="modal ">
      <transition name="modal-animation-inner">
        <div v-show="modalActive" class="modal-inner">
          <iconify-icon @click="close" class="icon" icon="fa:close"></iconify-icon>
          <!-- Modal Content -->
          <slot />
         
        </div>
      </transition>
    </div>
  </transition>

</template>

<script>
export default {
  props: ['modalActive'],
  setup(props, {emit}) {
    const close = () =>{
      emit("close");
    }  ;
    return { close }
  },

};
</script>


<style lang="scss" scoped>
  .modal-animation-enter-active,
  .modal-animation-leave-active{
    transition: opacity .3s cubic-bezier(0.52, 0.02, 0.19, 1.02);
  }

  .modal-animation-enter-from,
  .modal-animation-leave-to {
    opacity: 0;
  }
  
  .modal-animation-inner-enter-active {
    transition: all .3s cubic-bezier(0.52, 0.02, 0.19, 1.02) 0.15s;
  }
  .modal-animation-inner-leave-active {
    transition: all .3s cubic-bezier(0.52, 0.02, 0.19, 1.02);
  }

  .modal-animation-inner-enter-from {
    opacity:0;
    transform:scale(0.8);
  }

  .modal-animation-inner-leave-to {
    transform:scale(0.8);
  }
  .modal{
   
    backdrop-filter: blur(12px);
    display: flex;
    justify-content: center;
    align-content: center;
    height: 100vh;
    width: 100vw;
    z-index: 21;
    position: fixed;
    top: 0;
    left: 0;
   

    .modal-inner {
     
      position: relative;
      display: flex;
      justify-content: center;
      align-content: center;
      // box-shadow: 0 4px 6px -1px rgba($color: #000000, $alpha: 0.1), 0 2px 4px -1px rgba($color: #000000, $alpha: 0.06);
      padding: 120px ;

        .icon{
          position:absolute;
          top:140px;
          right:140px;
          font-size:20px;
          
          cursor: pointer;

          &:hover{
            color: rgb(248 113 113);
          }
        }

       
      }
  }
</style>