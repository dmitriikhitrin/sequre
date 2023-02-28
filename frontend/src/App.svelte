<script lang="ts">
  import { onMount } from "svelte";
  import { v4 as uuidv4 } from 'uuid';

  interface Message {
    text: string,
    date: number,
    id: string
  }

  let client_id;

  let message: string;
  let messages: Message[] = [];

  let socket: WebSocket;

  let isSocketConnectionEstablished:boolean = false;
  // Define a function to handle the button click event
function handleButtonClick() {
    // Connect to the websocket
    socket = new WebSocket("ws://localhost:8000/ws");
  
    // Add event listeners to handle the websocket events
    socket.addEventListener("open", () => {
      console.log("WebSocket connection established");
      isSocketConnectionEstablished = true;
    });
  
    socket.addEventListener("message", (event) => {
      console.log(`Received message: ${event.data}`);
      let msgObject = JSON.parse(event.data);
      console.log(msgObject);

      console.log(msgObject.id);
      
      // TODO: implement closing
      messages = [...messages, msgObject]
    });
  
    socket.addEventListener("close", () => {
      console.log("WebSocket connection closed");
      isSocketConnectionEstablished = false;
      messages = []; 
    });
  }

  function closeSocketConnection(){
    if (!isSocketConnectionEstablished) return;
    messages = [];
    socket.close();
  }

    // Define a function to send a message over the websocket
    function sendMessage() {

      const sendingMsg: Message = {
        text: message,
        date: Date.now(),
        id: client_id
      }
      socket.send(JSON.stringify(sendingMsg));
      message = ""
    }

  onMount(()=>{
    client_id = uuidv4();
    console.log(client_id);
    
  })

</script>

<main class="p-20 container mx-auto">
  {#if isSocketConnectionEstablished}
    <div class="flex flex-row max-w-md justify-between items-center">
      <p class="my-8 font-semibold text-sm text-green-800 px-4 py-2 rounded-md bg-green-100">Connection Established</p>
      <button on:click={()=> closeSocketConnection()} class="px-4 py-2 text-red-800 bg-red-100 rounded-md">Kill chat</button>
    </div>
    {:else}
    <div class=" my-10">
      <button on:click={()=>handleButtonClick()} class="btn-primary">Create a socket</button>
    </div>
  {/if}



<div class="max-w-sm mx-auto">
  {#each messages as msg}
    <p class=" {msg.id === client_id ? "text-right" : "text-left"} my-1"><span class="{msg.id === client_id ? "message-out" : "message-in"}">{msg.text}</span></p>
  {:else}
    <p>No messages today!</p>
  {/each} 

  <div class="flex items-center py-2 px-3 bg-gray-50 rounded-lg dark:bg-gray-700">
      <textarea bind:value={message} id="chat" rows="1" class="block mx-4 p-2.5 w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-sky-500 focus:border-sky-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Your message..."></textarea>
          <button on:click={()=> sendMessage()} type="submit" class="inline-flex justify-center p-2 text-sky-600 rounded-full cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600">
          <svg class="w-6 h-6 rotate-90" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path></svg>
      </button>
  </div>
</div>


  <div class="my-20">
    {#each messages as msg}
      <p>{msg.text}</p>
    {:else}
      <p>No messages today!</p>
    {/each}
  </div>

  {isSocketConnectionEstablished ? "CONNECTED" : "NOT CONNECTED"}

</main>


