import './App.css';
import axios from 'axios';
import { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const evtSource = new EventSource('http://localhost:5000/events');
    evtSource.addEventListener('dataUpdate', (e) => {
      console.log('evt : ', JSON.parse(e.data))

      setData(JSON.parse(e.data))
    });

    axios
      .get('http://localhost:5000/', {
        headers: { 'Access-Control-Allow-Origin': '*' },
      })
      .then(
        (result) => {
          console.log('axios : ', result.data)
          setData(result.data)
        },
        (error) => console.log(error)
      );
  }, [])

  return (
    <>
      {data.map((v, i) => {
        return (
          <div key={i} style={{display: 'flex', gap: 20}}>
            <div style={{width: '10%', display: 'flex', gap: 20}}>
              <strong>ID</strong>
              <span>{v.id}</span>
            </div>
            <div style={{width: '20%', display: 'flex', gap: 20}}>
              <strong>NAME</strong>
              <span>{v.name}</span>
            </div>
            <div style={{width: '40%', display: 'flex', gap: 20}}>
              <strong>ADDRESS</strong>
              <span>{v.address}</span>
            </div>
            <div style={{width: '30%', display: 'flex', gap: 20}}>
              <strong>USER ID</strong>
              <span>{v.userId}</span>
            </div>
          </div>
        )
      })}
    </>
  );
}

export default App;
