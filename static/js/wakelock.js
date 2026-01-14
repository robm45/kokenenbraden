// script to prevent the screensaver
let wakeLock = null;       
const button = document.getElementById('wake-lock-button');
                           
async function toggleWakeLock() {
  if (wakeLock) {          
    // Uitschakelen        
    await wakeLock.release();
    wakeLock = null;       
    button.textContent = "🟢 Scherm aanhouden: UIT";
  } else {                 
    try {                  
      wakeLock = await navigator.wakeLock.request("screen");
      button.textContent = "🔵 Scherm aanhouden: AAN";
                           
      // Heractiveren als tab focus terugkrijgt
      document.addEventListener("visibilitychange", async () => {
        if (wakeLock !== null && document.visibilityState === "visible") {
          wakeLock = await navigator.wakeLock.request("screen");
        }                  
      });                  
    } catch (err) {        
      alert("Wake Lock niet ondersteund of geweigerd: " + err);
    }                      
  }                        
}                          
                           
button.addEventListener('click', toggleWakeLock);
