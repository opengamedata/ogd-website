export default class APIResponse {
   /**
    * 
    * @param {Object.<string, any>?} response_object 
    */
   constructor(response_object) {
      if (response_object != null) {
         /** @type {string} */
         this.req_type    = response_object.data.type;
         /** @type {object} */
         this.values_dict = response_object.data.val;
         /** @type {string} */
         this.message     = response_object.data.msg;
         /** @type {int} */
         this.status      = response_object.status;
      }
      else {
         this.message     = "FAIL: Response object was null";
         this.status      = null;
         this.req_type    = null;
         this.values_dict = {};
      }
   }

   get RequestType() {
      return this.req_type;
   }
   get Values() {
      return this.values_dict;
   }
   get Message() {
      return this.message;
   }
   get Status() {
      if (this.status >= 200 && this.status < 300) {
         return "SUCCESS";
      }
      else {
         return "ERROR";
      }
   }
   get asDict() {
      return {
         type: this.req_type,
         val: this.values_dict,
         msg: this.message,
         status: this.status
      }
   }
}