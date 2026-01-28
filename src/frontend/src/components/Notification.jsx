const Notification = ({ message }) => {
  if (message === null) {
    return null
  }
  const notificationStyle = {
    color: 'green',
    fontStyle: 'italic',
    fontSize: '20px'
  }

  return (
    <div style={notificationStyle}>
      {message}
    </div>
  )
}

export default Notification