class PostForm(Form):
    body = TextAreaField("写下今天的心情吧", validator = [DataRequired()])
    submit = SubmitField("submit")

