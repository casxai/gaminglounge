import Pusher from 'pusher-js';

export const pusher = new Pusher('122926f4663427b23929', {
    cluster: 'ap1',
    forceTLS: true
  });

