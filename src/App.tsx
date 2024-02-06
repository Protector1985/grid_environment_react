import React from 'react';
import GameCanvas from './components/GameCanvas/GameCanvas';
import css from './styles/styles.module.css'
import { makeMove } from './utils';

function App() {

  const [playerPosition, setPlayerPosition] = React.useState(15)

 
    setInterval(() => {
      makeMove("UP", playerPosition, setPlayerPosition)
    }, 2000)
    

  

  return (
    <div className={css.wrapper}>
      <GameCanvas gridSize={45} playerPosition={playerPosition} />
    </div>
  );
}

export default App;
