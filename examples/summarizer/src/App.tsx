import React, { useState } from "react";
import {
  Button,
  Box,
  Textarea,
  VStack,
  HStack,
  Text,
  Spinner
} from "@chakra-ui/react";
import { Formik, Form, Field, FormikProps, FieldProps } from "formik";
import axios from "axios";

import { Configuration, OpenAIApi } from "openai";

console.log(
  "process.env.REACT_APP_OPENAI_API_KEY",
  process.env.REACT_APP_OPENAI_API_KEY,
  "process.env.REACT_APP_WALE_API_KEY",
  process.env.REACT_APP_WALE_API_KEY
);

const configuration = new Configuration({
  apiKey: process.env.REACT_APP_OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

interface FormValues {
  textarea: string;
}

function App() {
  const [loading, setLoading] = useState(false);

  async function onSubmit(values: FormValues) {
    setLoading(true);
    try {
      console.log('submitting', { text: values.textarea });
      const res = await axios.post(
        "https://api.trywale.com/logger",
        {
          api_key: process.env.REACT_APP_WALE_API_KEY,
          inputs: {
            text: values.textarea,
            mode: "short",
          },
          output: 'Summarize: ' + values.textarea,
          model_config: {
            "model": "text-davinci-002",
            "max_tokens": 64,
            "temperature": 0.2,
          },
          total_tokens: 64,
          person_id: "uid-user123",
          task_id: 'tid-task123',
        }
      );
      
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  }

  const initialValues: FormValues = {
    textarea: ""
  };

  const validate = (values: FormValues): Partial<FormValues> => {
    const errors: Partial<FormValues> = {};
    if (!values.textarea) {
      errors.textarea = "Textarea is required";
    }
    return errors;
  };

  return (
    <Box>
      <Formik initialValues={initialValues} onSubmit={onSubmit} validate={validate}>
        {({ errors, touched }: FormikProps<FormValues>) => (
          <Form>
            <VStack w="full" alignItems="center" justifyContent="center" mt={10}>
              <Text fontSize="xl" fontWeight="bold">
                Summarizer Demo
              </Text>
              <VStack w="xl" px={3}>
                <Field name="textarea">
                  {({ field }: FieldProps<string, FormValues>) => (
                    <Textarea {...field} placeholder="Summarize this ..." w="full" />
                  )}
                </Field>
                {/* {errors.textarea && touched.textarea && (
                  <Text color="red">{errors.textarea}</Text>
                )} */}
                <Button
                  w="full"
                  type="submit"
                  as="button"
                  disabled={loading}
                  isLoading={loading}
                  loadingText="Loading..."
                  spinner={<Spinner size="sm" />}
                >
                  Submit
                </Button>
              </VStack>
            </VStack>
          </Form>
        )}
      </Formik>
    </Box>
  );
}

export default App;
