import React, { useEffect, useCallback, useState, useLayoutEffect } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Avatar } from 'react-native-elements';
import { GiftedChat, Actions, Bubble, Composer, InputToolbar } from 'react-native-gifted-chat';
import { launchCamera, launchImageLibrary } from 'react-native-image-picker';
import { Icon } from 'react-native-elements';
import uuid from 'react-native-uuid';
import QuickReplies from 'react-native-gifted-chat/lib/QuickReplies';




//Chat Interface
const Chat = ({ navigation }) => {

    //Add hours to Date() function because Date() uses GMT timezone
    Date.prototype.addHours = function(h) {
        this.setTime(this.getTime() + (h*60*60*1000));
        return this;
    } 
    
    //Bot Info
    const Bot = {
        _id: 'faqbot',
        name: 'FAQ Bot',
        avatar: 'https://placeimg.com/140/140/any',
    };

    //User Info (have to change using gdex id or anonymous id)
    const User = {
        _id: 1,
        email: 't.hazeeq@gmail.com',
        name: 'Hazeeq',
        avatar: 'https://placeimg.com/140/140/any'
    }
    
    const renderQuickReplies = (props)=>{
        return (
            <QuickReplies
                {...props}
                quickReplyStyle={{
                    backgroundColor: "#DCF8C6",
                }}
            />
        )
    }

    const renderInputToolbar = (props)=>{
        return (
            <InputToolbar
                {...props}
                containerStyle={{ backgroundColor: "white", }}
                renderComposer={props1 => ( <Composer {...props1} textInputStyle={{ color: "black"}} /> )}
            />
        )
    }
    
    const renderBubble = (props)=>{
        return (
            <Bubble
                {...props}
                wrapperStyle={{
                    left: {
                      backgroundColor: '#DCF8C6',
                    },
                    right: {
                      backgroundColor: "#075E54",
                    },
                  }}
            />
        )
    }

    //Send Image Function (not sending to any database for now)
    const renderActions = (props) => {
        return (
            <Actions
                {...props}
                options={{

                    //Take picture from camera
                    ['Take Picture']: async(props)=>{
                        try{
                            const result = await launchCamera({mediaType:'photo'});
                            if(result){
                                console.log(result.assets[0].uri);
                                onSend([{
                                    _id: uuid.v4(),
                                    createdAt: new Date().addHours(8),
                                    image: result.assets[0].uri,
                                    user: User,
                                }]);
                            }else{
                                console.log('close camera');
                            }
                            
                        }catch(err){
                            console.log('close camera');
                            throw err;
                        }
                    },

                    //Take picture from gallery
                    ['Send Image']: async(props)=>{
                        try{    
                            const result = await launchImageLibrary({mediaType: 'photo',});

                            if(result){
                                console.log(result.assets[0].uri);
                                onSend([{
                                    _id: uuid.v4(),
                                    createdAt: new Date().addHours(8),
                                    image: result.assets[0].uri,
                                    user: User,
                                }]);
                            }else{
                                console.log('close gallery');
                            }
                        } catch (err){
                            console.log('close gallery');
                            throw err;
                        }
                    },

                    //Cancel action
                    Cancel: (props) => { console.log("Cancel") }
                }}

                icon={() => (
                    <Icon name={'attachment'} size={28} />
                )}

                onSend={args => console.log(args)}
            />
        )
    };
    
    const [messages, setMessages] = useState([]);

    useLayoutEffect(() => {
        navigation.setOptions({

            //User's Avatar
            headerLeft: () => (
                <View style={{ marginLeft: 20 }}>
                    <Avatar
                        rounded
                        source={{
                            uri: 'https://placeimg.com/140/140/any',
                        }}
                    />
                </View>
            ),
        })
    }, [navigation]);

    useEffect(() => {
        //Starting message
        setMessages([
            {
                _id: uuid.v4(),
                text: "Sila taip 'Hi' untuk tanya soalan.",
                createdAt: new Date().addHours(8),
                user: Bot,
            },
            {
                _id: uuid.v4(),
                text: "Ini ialah bot sembang FAQ automatik.",
                createdAt: new Date().addHours(8),
                user: Bot,
            }
        ])
        
    }, []);

    //Post message to Botpress API and receive response
    const handleOnSend = async({messages}) => {
        try{

            let text = '';
            id = messages[0].user._id;
            text = messages[0].text;

            const axios = require('axios').default;

            //Post Body
            const data = JSON.stringify({ 'type':'text', 'text': text});

            //Post Config
            const config = {
                method: 'post',
                url: 'http://10.0.2.2:3000/api/v1/bots/faqbot/converse/'+id+'/',
                headers: { 
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InQuaGF6ZWVxQGdtYWlsLmNvbSIsInN0cmF0ZWd5IjoiZGVmYXVsdCIsInRva2VuVmVyc2lvbiI6MSwiaXNTdXBlckFkbWluIjp0cnVlLCJpYXQiOjE2NTQ1ODcwNjEsImV4cCI6MTY1NDU5MDY2MSwiYXVkIjoiY29sbGFib3JhdG9ycyJ9.gnKW6UBzCfwFhlpXGY6YHYM6D5G8h17-JC-Nyo55adE', 
                    'Content-Type': 'application/json'
                },
                data: data
                    
            };

            const response = await axios(config);

            if(response.status === 200){
                result = response.data;
                return result;
            }
        }catch(err){
            console.error(err);
        }
    }

    //Output BotPress response
    const botResponse = async(messages) =>{

        await handleOnSend({messages}).then(result=>result).catch(error=>{console.error(error)});
        
        result.responses.map((response)=>{
            console.log("Response: "+JSON.stringify(response));
            let msg = {};
            //Text Response
            if(response.type == 'text'){
                msg = {
                    _id: uuid.v4(),
                    createdAt: new Date().addHours(8),
                    text: response.text,
                    user: Bot,
                }

            //Single-choice Response
            }else if(response.type=='single-choice'){
                response.choices.map((choice)=>{
                    choice['_id'] = uuid.v4()
                    choice['user'] = User
                })
                msg = {
                    _id: uuid.v4(),
                    createdAt: new Date().addHours(8),
                    text: response.text,
                    quickReplies: {
                        type: 'radio',
                        keepIt: false,
                        values: response.choices,
                    },
                    user: Bot,
                }

            //Image Response
            }else if(response.type == 'image'){
                let imageUrl = response.image;
                let url = imageUrl.replace("localhost", "10.0.2.2");
                msg =
                {
                    _id: uuid.v4(),
                    createdAt: new Date().addHours(8),
                    text: response.title,
                    image: url,
                    user: Bot,
                }
            
            //Card Response
            }else if(response.type == 'card'){
                msg = []
                
                if(response.actions){
                    response.actions.reverse().map((action)=>{
                        msg.push({
                            _id: uuid.v4(),
                                createdAt: new Date().addHours(8),
                                text: action.url,
                                user: Bot,
                        })
                    })
                }
                if(response.image){
                    let imageUrl = response.image;
                    let fiximageurl = imageUrl.replace("localhost", "10.0.2.2");
                    msg.push({
                        _id: uuid.v4(),
                            createdAt: new Date().addHours(8),
                            image: fiximageurl,
                            user: Bot,
                    })
                }
                if(response.subtitle){
                    msg.push({
                        _id: uuid.v4(),
                            createdAt: new Date().addHours(8),
                            text: response.subtitle,
                            user: Bot,
                    })
                }
                if(response.title){
                    msg.push({
                        _id: uuid.v4(),
                            createdAt: new Date().addHours(8),
                            text: response.title,
                            user: Bot,
                    })
                }
                
            }else if(response.type == 'carousel'){
                msg = []
                response.items.reverse().map((item)=>{

                    if(item.actions){
                        item.actions.reverse().map((action)=>{
                            msg.push({
                                _id: uuid.v4(),
                                    createdAt: new Date().addHours(8),
                                    text: action.url,
                                    user: Bot,
                            })
                        })
                    }
                    if(item.image){
                        let imageUrl = item.image;
                        let fiximageurl = imageUrl.replace("localhost", "10.0.2.2");
                        msg.push({
                            _id: uuid.v4(),
                                createdAt: new Date().addHours(8),
                                image: fiximageurl,
                                user: Bot,
                        })
                    }
                    if(item.subtitle){
                        msg.push({
                            _id: uuid.v4(),
                            createdAt: new Date().addHours(8),
                            text: item.subtitle,
                            user: Bot,
                        })
                    }
                    if(item.title){
                        msg.push({
                    
                            _id: uuid.v4(),
                            createdAt: new Date().addHours(8),
                            text: item.title,
                            user: Bot,
                        });
                    }
                })
            //Else response
            }else{
                msg ={
                    _id: uuid.v4(),
                    createdAt: new Date().addHours(8),
                    text: 'Error',
                    user: Bot,
                };
            }

            setMessages(previousMessages => GiftedChat.append(previousMessages, msg))
        })
        
    }

    
    //Receive message and append to previous message
    const onSend = useCallback((messages = []) => {

        //Change quick replies json to normal message json
        if(!messages[0].text)
        {
            messages[0].text = messages[0].title;
            delete messages[0].title;
            delete messages[0].value
        }
        
        setMessages(previousMessages => GiftedChat.append(previousMessages, messages));
        
        if(!messages[0].image){
            botResponse(messages);
        }

    }, []);

    //Return gifted chat class
    return (
        <GiftedChat
            messages={messages}
            showAvatarForEveryMessage={true}
            quickReplies={messages.quickReplies}
            onSend={messages => onSend(messages)}
            onQuickReply={quickReply => onSend(quickReply)}
            //render take picture action (not available as it doesnt send the picture to any database)
            //renderActions={ ()=>renderActions() }
            renderBubble={(props)=>renderBubble(props)}
            renderInputToolbar={(props)=>renderInputToolbar(props)}
            renderQuickReplies={(props)=>renderQuickReplies(props)}
            user={User}
        />
    );
}

export default Chat;