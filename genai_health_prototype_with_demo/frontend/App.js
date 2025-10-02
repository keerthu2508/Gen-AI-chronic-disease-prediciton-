/**
 * React Native skeleton for the GenAI Chronic Care app.
 * - Local storage (AsyncStorage) used for offline medication reminders.
 * - Screens: Home, Reminders, VitalsEntry, Messages
 * This is a simplified single-file starter for prototyping.
 */
import React, {useEffect, useState} from 'react';
import {SafeAreaView, View, Text, Button, TextInput, FlatList, Alert} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const MED_KEY = '@med_reminders';

const App = () => {
  const [meds, setMeds] = useState([]);
  const [newMed, setNewMed] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const raw = await AsyncStorage.getItem(MED_KEY);
        if (raw) setMeds(JSON.parse(raw));
      } catch (e) {
        console.warn(e);
      }
    })();
  }, []);

  const addMed = async () => {
    if (!newMed) return;
    const next = [...meds, {id: Date.now().toString(), name: newMed, schedule: '09:00'}];
    setMeds(next);
    await AsyncStorage.setItem(MED_KEY, JSON.stringify(next));
    setNewMed('');
    Alert.alert('Saved', 'Medication reminder saved locally for offline use');
  };

  const renderItem = ({item}) => (
    <View style={{padding:8, borderBottomWidth:1}}>
      <Text>{item.name}</Text>
      <Text>Schedule: {item.schedule}</Text>
    </View>
  );

  return (
    <SafeAreaView style={{flex:1, padding:16}}>
      <Text style={{fontSize:20, fontWeight:'bold'}}>GenAI Chronic Care - Prototype</Text>
      <View style={{marginVertical:12}}>
        <TextInput placeholder='New medication name' value={newMed} onChangeText={setNewMed} style={{borderWidth:1,padding:8}} />
        <Button title='Add Reminder (offline)' onPress={addMed} />
      </View>
      <FlatList data={meds} keyExtractor={i=>i.id} renderItem={renderItem} />
    </SafeAreaView>
  );
};

export default App;
