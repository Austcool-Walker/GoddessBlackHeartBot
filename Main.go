package main

import (
	"fmt"
	"strings"
	"github.com/bwmarrin/discordgo"
	"os"
	"os/signal"
	"syscall"

)

// Variables
var Prefix = "X"

func main() {
	// Create a new Discord session using the provided bot token.
	dg, err := discordgo.New("Bot " + "NjkzNTY4MjYyODEzOTA5MDcy.Xn-9xw.In04gEB4OcS4Xmn1aDDj_phboY0")
	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return
	}
	
	dg.AddHandler(readyEvent)
	dg.AddHandler(messageCreate)
	
	// Open a websocket connection to Discord and begin listening.
	err = dg.Open()
	if err != nil {
		fmt.Println("error opening connection,", err)
		return
	}
	
	fmt.Println("Bot is starting to run...")
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-sc
	dg.Close()
}

// Ready Event
func readyEvent(s *discordgo.Session, m *discordgo.Ready) {
	fmt.Println("Bot Ready and Gay.  Press CTRL-C to exit.")
}


// This function will be called (due to AddHandler above) every time a new
// message is created on any channel that the authenticated bot has access to.
func messageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {
	// Ignore all messages created by the bot itself
	// This isn't required in this specific example but it's a good practice.
	if m.Author.ID == s.State.User.ID {
		return
	}
	
	if !strings.HasPrefix(m.Content, Prefix) {
		return
	}
	
	// If the message is "ping" reply with "Pong!"
	if m.Content == Prefix + "ping" {
		s.ChannelMessageSend(m.ChannelID, "Pong!")
	}
	
	// If the message is "pong" reply with "Ping!"
	if m.Content == Prefix + "pong" {
		s.ChannelMessageSend(m.ChannelID, "Ping!")
	}
}

