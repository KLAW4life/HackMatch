import PropTypes from 'prop-types'

function Card(props){

    return(
        <span className ="card">
            <p className = "card-name">{props.info}</p>
            <img className = "card-image" alt='an image' src ={props.image}></img>
        </span>
    );

}

Card.propTypes ={
    info : PropTypes.string,
    image: PropTypes.string
}

export default Card