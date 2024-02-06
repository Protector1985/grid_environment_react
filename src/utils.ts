export function makeMove(direction:string, currentPosition:number, setter:any) {
    
    function hitWall() {
        switch(direction) {
            case "RIGHT": 
                console.log(currentPosition + 1 !== 9)
                if(currentPosition + 1 === 9 || currentPosition + 1 === 17 ||currentPosition + 1 === 26 ||currentPosition + 1 === 35 ||currentPosition + 1 === 46) {
                    return true
                } else {
                    
                    return false
                }
                
            case "LEFT": 
                    if(currentPosition - 1 === -1 || currentPosition - 1 === 8 || currentPosition - 1 === 17 || currentPosition - 1 === 26 || currentPosition - 1 === 35) {
                        return true
                    } else {
                        return false
                    }

            case "UP": 
                    if(currentPosition - 9 >= 0) {
                        return false
                    } else {
                        return true
                    }
            case "DOWN": 
                    if(currentPosition + 9 <= 45) {
                        return false
                    } else {
                        return true
                    }  
                
            }
        }
    
    
    switch(direction) {
        case "LEFT":
            if(!hitWall())
                setter(currentPosition - 1)
           
            break;
        case "RIGHT":
            if(!hitWall())
                setter(currentPosition + 1)
            
            break;
        case "UP":
            if(!hitWall())
                setter(currentPosition - 9)
            
            break;
        case "DOWN":
            if(!hitWall())
                setter(currentPosition + 9)
           
            break;
        default: setter(currentPosition)
    }

}