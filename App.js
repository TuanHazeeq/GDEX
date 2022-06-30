import React from 'react';
import { StyleSheet } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import ChatScreen from './screens/Chat';


const Stack = createStackNavigator();

const App = () => {
    return ( 
        <NavigationContainer>
            <Stack.Navigator>
                <Stack.Screen name='Chat' component={ChatScreen}/>
            </Stack.Navigator>
        </NavigationContainer>
    );
};

export default App;