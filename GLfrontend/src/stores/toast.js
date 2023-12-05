import {defineStore} from 'pinia'

// js for alerts and errors
export const useToastStore = defineStore({
    id: 'toast',

    state: () => ({
        ms: 0, //how many milliseconds
        message: '', //the message
        classes: '', //green if success and red if failure
        isVisible: false //default is false
    }),

    actions: { // to manipulate the value above
        showToast(ms, message, classes) {
            this.ms = parseInt(ms)
            this.message = message
            this.classes = classes
            this.isVisible = true
            // this.classes = 'transition-opacity duration-300 origin-top-right'
            setTimeout(() => {
                this.classes += ' -translate-y-28'
            }, 10)

            setTimeout(() => {
                this.classes = this.classes.replace('-translate-y-28', '')
            }, this.ms - 500)

            setTimeout(() => {
                this.isVisible = false
            }, this.ms)
        },
        
    }
})