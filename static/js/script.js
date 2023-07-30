// Example POST method implementation:
async function postData(url = "", data = {}) {

     const response = await fetch(url, {

      method: "POST", // *GET, POST, PUT, DELETE, etc.
 
      headers: {

        "Content-Type": "application/json",
        
      },

      body: JSON.stringify(data), 

    });
    return response.json(); 
  }



btn.addEventListener("click",async()=>{

    question = document.getElementById("question").value ;
    solution.innerHTML = "Loading....."
  
    
    let result = await postData("/api",{"question":question})
   
    solution.innerHTML = result.answer

    

    
    
})